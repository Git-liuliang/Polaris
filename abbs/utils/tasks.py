import time
from celery import task,Celery

from celery import Task,Celery,task


# class MyTask(Task):
#     def on_success(self, retval, task_id, args, kwargs):
#         print 'task done: {0}'.format(retval)
#         return super(MyTask, self).on_success(retval, task_id, args, kwargs)
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print 'task fail, reason: {0}'.format(exc)
#         return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)
#
# app = Celery('tasks',  backend='redis://:xinwei1234%@172.18.3.181:6380/0', broker='redis://:xinwei1234%@172.18.3.181:6380/0')
#
# @app.task(base=MyTask)
# def add(x, y):
#     return x + y
@task
def add(x,y):
    return x+y