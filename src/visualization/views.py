from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime
import plotly.express as px
import pandas as pd

from main.models import DiaryEntry


@login_required(login_url='/login')
def visualization(request):
    entries = DiaryEntry.objects.filter(author=request.user).values()
    positives = []
    negatives = []
    neutrals = []

    dates = []
    moods = []
    value = []

    for note in entries:
        note['created_at'] = note['created_at'].date()
        if note['sentiment_label'] == 'positive':
            positives.append(note)
        elif note['sentiment_label'] == 'negative':
            negatives.append(note)
        else:
            neutrals.append(note)

        dates.append(note['created_at'])
        value.append(1)
        moods.append(note['sentiment_label'])
    fig1 = px.pie(
        values=[len(negatives), len(neutrals), len(positives)],
        names=['Negative', 'Neutral', 'Positive']
    )
    fig1.update_layout(
        title=dict(
            text='<b>Overall Statistics</b>',
            x=0.5,
            font_size=20,
            font_color='#212529'
        ),
    )
    fig1.update_traces(
        marker=dict(colors=['#dc3545', '#0d6efd', '#20c997'])
    )
    pie_chart = fig1.to_html()

    df = pd.DataFrame([dates, value, moods], index=['date', 'value', 'mood']).T
    start = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())

    dates1 = []
    value1 = [0] * 7
    moods1 = ['positive'] * 7
    for i in range(7):
        dates1.append(start + datetime.timedelta(days=i))
        if i == 6:
            finish = start + datetime.timedelta(days=i)
    df1 = pd.DataFrame([dates1, value1, moods1], index=['date', 'value', 'mood']).T
    df = pd.concat([df, df1], axis=0)
    df = df[(df['date'] >= start) & (df['date'] <= finish)]
    df = df.groupby(['date', 'mood']).agg({'value': 'sum'}).reset_index()
    df = df.sort_values('date')
    df['date'] = df['date'].apply(lambda x: x.strftime('%a, %d %b'))

    fig2 = px.bar(
        df,
        x='date',
        y='value',
        color='mood',
        color_discrete_map={"positive": "#dc3545", "negative": "#0d6efd", 'neutral': '#20c997'},
    )
    new_names = {'positive': 'Positive', 'negative': 'Negative', 'neutral': 'Neutral'}
    fig2.for_each_trace(lambda t: t.update(name=new_names[t.name]))
    fig2.update_layout(
        yaxis=dict(
            title='',
            fixedrange=True,
            tickvals=[i for i in range(min(df.value), max(df.value) + 2)]
        ),
        xaxis=dict(
            title='',
            fixedrange=True
        ),
        title=dict(
            text='<b>Weekly Statistics</b>',
            x=0.5,
            font_size=20,
            font_color='#212529'
        ),
        legend_title=''
    )
    bar_chart = fig2.to_html()

    context = {
        'notes': entries,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart
    }
    return render(request, 'vis.html', context)


@login_required(login_url='/login')
def notes(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'notes.html', context)


@login_required(login_url='/login')
def positives(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'positives.html', context)


@login_required(login_url='/login')
def negatives(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'negatives.html', context)


@login_required(login_url='/login')
def neutrals(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'neutrals.html', context)
