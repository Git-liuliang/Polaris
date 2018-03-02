# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,redirect
from abbs import models
import json
import pickle
from utils import filehander
from abbs import tasks


from django.http import JsonResponse

def login(request):

    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        input_valid_codes=request.POST.get("valid_code")

        # 校验验证码
        keep_valid_codes=request.session.get("keep_valid_codes")
        '''
        1  拿到cookie中sessionid对应的随机字符串
        2  在django-session表中过滤记录
        3  .... 
        '''

        login_response={"user":None,"error_msg":""}


        if keep_valid_codes.upper()==input_valid_codes.upper():
            user=auth.authenticate(username=user,password=pwd)
            if user:
                auth.login(request,user)
                login_response["user"]=user.username
                filehander.createdir(user.username)
            else:
                login_response["error_msg"] = "username or password error!"
        else:
            login_response["error_msg"]="valid_code error!"
        import json
        return HttpResponse(json.dumps(login_response))
    else:
        return render(request,"login.html")


def get_valid_img(request):

    from abbs.utils import valid_code

    data=valid_code.get_valid_value(request)

    return HttpResponse(data)


@login_required
def index(request):
    print("==", dir(request.user))
    res = []
    user_obj = models.UserInfo.objects.filter(username=request.user.username).first()
    print user_obj
    feut = models.Inventory2UserInfo.objects.filter(user=user_obj.nid)
    print feut
    for i in feut:
        sd = models.Inventory.objects.filter(nid=i.machine_id).first()
        res.append(sd)



    return render(request, "index.html",{"res":res})



def three(request):
    import time
    from abbs import tasks
    import sys

    # if request.method == "POST":


    # if request.method == "POST":
    result = tasks.add.delay(4, 4)
    print type(result)
    print result.task_id
    res = pickle.dumps(result)
    request.session[result.task_id] = res
    # request.session.get(result.task_id)
    # while not result.ready():
    #     time.sleep(1)
    #     print result.state
    # print 'task done: {0}'.format(result.get())
    return render(request, "demo.html", {"res": result})
        # return render(request,"demo.html")
    # while not res.ready():
    #     time.sleep(3)
    # print 'task done: {0}'.format(res.get())

def process(request):

    jobid = request.POST.get("jobid")
    print jobid
    # ppp = request.session.get(jobid)
    # res = pickle.loads(ppp)
    rest = models.task_info.objects.filter(task_id=jobid).first()
    # print rest.task_result.state
    mid = pickle.loads(rest.task_result)
    res = mid
    print 'aaaaa',res.state
    print "-----------",res.result
    import json
    return HttpResponse(json.dumps({"status":res.state,"result":res.result}))



def createuser(request):

    user = models.UserInfo.objects.create_user(username="alex",password="xinwei")
    return HttpResponse("ok")

def udiff(request):
    if request.method == "POST":
        s = request.POST.get("ip_list")
        d = request.FILES.get("avatar_img")
        filepath = request.POST.get("filepath")

        if s == '' or d == ' ' or filepath == '':
            print 'aaaaaaaaa'
            status = 1
            error_message = "项目不能为空"
            return HttpResponse(json.dumps({"status": status, "error_message": error_message}))

        else:

            update_file = filehander.store_upload_file(request.user.username, d)
            remote_path = request.POST.get("filepath")
            ip_list = request.POST.get("ip_list")
            result = tasks.add.delay(2, 4)
            print type(result)
            print result.task_id
            res = pickle.dumps(result)
            models.task_info.objects.create(task_id=result.task_id,task_args=remote_path,task_result=res)
            # res = pickle.dumps(result)
            # request.session[result.task_id] = res
            status = 0

            return HttpResponse(json.dumps({"status": status, "error_message": "ok","taskid":result.task_id}))



    res = []
    user_obj = models.UserInfo.objects.filter(username=request.user.username).first()
    # print user_obj
    feut = models.Inventory2UserInfo.objects.filter(user=user_obj.nid)
    # print feut
    for i in feut:
        sd = models.Inventory.objects.filter(nid=i.machine_id).first()
        res.append(sd)


    task_list = models.task_info.objects.all()

    return render(request,"udiff.html",{"res":res,"task_list":task_list})
