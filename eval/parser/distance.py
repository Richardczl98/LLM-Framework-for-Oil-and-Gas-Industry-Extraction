import numpy as np

from model.chat_openai import openai_client
from model import models
from lib.my_logger import logger
from eval.parser.parser_utils import COSIN_SIMILARITY_THREADHOLD


def is_similar_text(text_1: str, text_2: str, thresholds: float = COSIN_SIMILARITY_THREADHOLD, method='cosin') -> bool:
    if method == 'cosin':
        if cosin_similarity(text_1, text_2) >= thresholds:
            return True
        else:
            return False
    else:
        logger.error(f"Compare method {method} is not supported. Only {method} can be use.")
        return False


def cosin_similarity(text_1: str, text_2: str, model: str = 'gpt-4') -> float:
    if models.is_model_openai(model):
        vec1 = openai_client.create_embedding(text_1)
        vec2 = openai_client.create_embedding(text_2)

        try:
            dist = vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        except ZeroDivisionError as err:
            logger.error(err)
            return -1
        return dist
    else:
        logger.error(f"Only GPT-4 model is supported but provided model is {model}")
        return -1
