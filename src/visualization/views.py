from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import plotly.express as px
import pandas as pd

from .models import Note, Analysis  # ToDo choose correct dir


# @login_required(login_url=TODO redirect to the correct login)
def visualization(request):
    # notes = Note.objects.filter(user=request.user.id).values() ToDo filter users
    notes = Note.objects.all()  # ToDO should be replaced with above one

    positives = []
    negatives = []
    neutrals = []

    dates = []
    moods = []
    value = []

    for note in notes:
        mood = Analysis.objects.get(note=note).mood
        if mood == 'positive':
            positives.append(note)
        elif mood == 'negative':
            negatives.append(note)
        else:
            neutrals.append(note)

        dates.append(note.date)
        value.append(1)
        moods.append(mood)

    fig1 = px.pie(
        values=[len(negatives), len(neutrals), len(positives)],
        names=['Negative', 'Neutral', 'Positive']
    )
    fig1.update_layout(
        title=dict(
            text='<b>Overall Statistics</b>',
            x=0.5,
            font_size=20,
            font_color='#000'
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
    df1 = pd.DataFrame([dates1, value1, moods1], index=['date', 'value', 'mood']).T
    df = pd.concat([df, df1], axis=0)
    df = df.groupby(['date', 'mood']).agg({'value': 'sum'}).reset_index()
    df = df.sort_values('date')
    df['date'] = df['date'].apply(lambda x: x.strftime('%a'))
    print(df)

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
            font_color='#000'
        ),
        legend_title=''
    )
    bar_chart = fig2.to_html()

    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart
    }
    return render(request, 'vis.html', context)


# @login_required(login_url=TODO redirect to the correct login)
def notes(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'notes.html', context)


# @login_required(login_url=TODO redirect to the correct login)
def positives(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'positives.html', context)


# @login_required(login_url=TODO redirect to the correct login)
def negatives(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'negatives.html', context)


# @login_required(login_url=TODO redirect to the correct login)
def neutrals(request):
    context = {
        'notes': notes,
        'positives': positives,
        'negatives': negatives,
        'neutrals': neutrals,
        'today': datetime.date.today
    }
    return render(request, 'neutrals.html', context)
