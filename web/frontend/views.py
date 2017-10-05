from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Workflow
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

import json
import requests
import os


# Create your views here. This login required decorator is to not allow to any view without authenticating
@login_required(login_url="login/")
def home(request):
    return render(request, "home.html")


# This takes in a user name and password to login. This view doesn't require any login
def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/homepage/')
    return render_to_response('login.html', context_instance=RequestContext(request))


# This is the view for main page - what users sees when we goes to cloudmatcher.io
def main_page(request):
    if request.POST:
        username = request.POST['form-username']
        password = request.POST['form-password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/frontend/homepage')
    return render(request, 'frontend/welcome/home.html')


# Once the user logs in to cloudmatcher.io - he sees this page as the first thing
@login_required
def homepage(request):
    return render(request, 'frontend/index.html')


# If the user refreshes or goes to home page after login then he will see the index page with updated details
@login_required
def index(request):
    username = request.user.username
    owner = User.objects.get(username=username)
    wf_list = Workflow.objects.filter(owner=owner).exclude(status='COMPLETED').exclude(status='ERROR').exclude(
        status='CANCELLED').order_by('id')

    context = {'wf_list': wf_list, 'state_description': state_description, 'username': username,
               'info_text': info_txt, 'wf_info': wf_info}

    return render(request, 'frontend/index.html', context)


# This view is used to handle new users who would like to register themselves to use CloudMatcher. It uses the
# registration form and the register.html page.
def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
        else:
            return render(request, 'userreg/register.html', {'form': form})
    return render(request, 'userreg/register.html')


# This method will send and receive metadata information from Meta Manager. This method will send the data from the
# web application to the meta core and will also process the response received from Meta Manager. This method should
# be very fast and should process all the calls quickly.
def send_receive_meta_manager(input_msg, method):

    # Sending the payload to the meta core by first converting the message into JSON format and then calling the
    # required MM method.
    send_message = json.dumps(input_msg)
    url = URL + method
    req = requests.post(url, data=send_message)

    # Receiving response from the meta core and processing it
    response = json.loads(req.text)
    return response


# Upload data view is used whenever the user wants to upload a new dataset. This view requires the user to
# login into the system.
@login_required
def upload_data(request):
    if request.method == 'POST':
        # Get the form data. For upload_data we know that UploadDatasetForm will be used.
        form = UploadDatasetForm(request.POST, request.FILES)
        # Check if the form is valid (whether all required information was filled or not by the user)
        if form.is_valid():
            # Fetching the workflow id from the request
            wf_id = request.POST['wfid']
            frag_id = request.POST['fragid']

            print('post request: ', request.POST)
            print('post info: ', wf_id)
            print('frag id: ', frag_id)

            # Save the uploaded file first in the uploaded files database
            in_file = request.FILES['docfile']
            submit_by = User.objects.get(username=request.user.username)
            _upload = UploadedFiles.objects.create(owner=submit_by)
            _upload.wf_id = wf_id
            _upload.doc_file = in_file
            _upload.save()

            logger.info('Uploaded file saved successfully to the database: ' + str(_upload.id))
            _up = UploadedFiles.objects.get(pk=_upload.id)
            file_loc = str(_up.doc_file.file.name)
            print(file_loc)

            # Fetching form information and create payload to call meta core rest api
            payload = {'user': request.user.username, 'wf_id': wf_id, 'file_name': request.POST['name'],
                       'info': request.POST['description'], 'file_loc': file_loc, 'celery_status': None,
                       'frag_id': frag_id}

            response_msg = send_receive_meta_manager(payload, 'workflow_update')
            return HttpResponse(json.dumps(response_msg), content_type="application/json")
        else:
            # If the form is not valid, it will be returned back to the user with status error
            logger.info("Invalid form")
    elif request.method == 'GET':
        owner = request.user.username
        # Checking if a Workflow id is already assigned or not
        using_wf_id = request.GET.get('wf_id', False)
        using_frag_id = request.GET.get('frag_id', False)

        # Creating payload to send as message to the create_workflow api of meta manager
        if not using_wf_id:
            payload = {'user': owner, 'template': 'upload_table'}
            received_msg = send_receive_meta_manager(payload, 'create_workflow')

            print('received_msg: ', received_msg)

            # Reading the workflow id and form details received from the Meta Manager (like the form)
            wf_id = received_msg['wf_id']
            message = received_msg['message'][0]
            print('Message: ', message)
            current_frag_id = int(message['current_frag_id'])
        else:
            wf_id = using_wf_id
            current_frag_id = using_frag_id

        print('GET request: ', wf_id, current_frag_id)

        # Returning the html page back to the user
        form = UploadDatasetForm(initial={'wfid': wf_id, 'fragid': current_frag_id})
        return render(request, 'frontend/create/upload_data.html', {'form': form, 'wf_id': wf_id,
                                                                    'frag_id': current_frag_id})

    msg = {
        'status': 'ERROR',
        'info': 'Error in processing the form post method!'
    }
    return HttpResponse(json.dumps(msg), content_type="application/json")


