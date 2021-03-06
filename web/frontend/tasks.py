from __future__ import absolute_import

from celery import shared_task

from celery.utils.log import get_task_logger

import subprocess

# testing
@shared_task
def addn(a, b):
    logger.info('Adding two numbers')
    return a + b, a - b


@shared_task
def multi(a, b):
    return a * b


@shared_task
def subt(a, b):
    return a - b


@shared_task
def divi(a, b):
    return a / b


@shared_task
def test_exception(a, b):
    d = 0
    try:
        d = a / b
    except Exception as e:
        print(e)

    return d
