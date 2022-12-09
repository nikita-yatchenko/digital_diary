import logging
from django.apps import AppConfig
from nlp_model_artifacts.bert import SentimentClassifier


class MainConfig(AppConfig):
    logger = logging.getLogger('MainConfig')

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    logger.info('IMPORT NLP MODEL')
    model = SentimentClassifier()
    logger.info('DONE WITH IMPORTING')
    logger.info('____________________________')
