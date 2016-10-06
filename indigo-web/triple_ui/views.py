""""Triple UI views

Copyright 2015 Archive Analytics Solutions

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import (
    render,
    redirect
)
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import (
    csrf_exempt,
    csrf_protect
)
from django.core.exceptions import PermissionDenied
from triple_ui.forms import (
    AddStatementsForm,
    QueryRepositoryForm,
    RepositoryForm
)
from django.contrib import messages

from triple_models.allegro_repository import (
    add_repository_statements,
    create_repository,
    delete_repository,
    delete_repository_statements,
    list_repositories,
    query_repository
)



@login_required()
def home(request):
    ok, ls_infos, _, msg = list_repositories()
    if not ok:
        messages.add_message(request, messages.ERROR, msg)
    ctx = {
        'is_admin': request.user.administrator,
        'repositories': [el.get('title', '') for el in ls_infos]
    }
    return render(request, 'triple_ui/repositories.html', ctx)


@login_required()
def view(request, repository):
    query = "select ?subject ?predicate ?object {?subject ?predicate ?object}"
    if request.method == 'POST':
        form = QueryRepositoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            query = data['query']
    else:
        form = QueryRepositoryForm()
    
    ok, r, _, msg = query_repository(repository, query)
    if not ok:
        messages.add_message(request, messages.ERROR, msg)
    ctx = {
        "form": form,
        'is_admin': request.user.administrator,
        'repository': repository,
        'results': r.json(),
        'query': query
    }
    return render(request, 'triple_ui/repository.html', ctx)

@login_required()
def delete_statements(request, repository):
    if request.method == "POST":
        ok, _, _, msg = delete_repository_statements(repository)
        if not ok:
            messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request, messages.INFO,
                                 "Statements have been deleted")
        #edited_repository_signal.send(None, user=request.user, repository=repository)
        return redirect('triple_ui:view', repository=repository)

    return render(request, 'triple_ui/delete_statements.html', {'repository': repository})


@csrf_exempt
def add_statements(request, repository):
    request.upload_handlers = [TemporaryFileUploadHandler()]
    return add_statements_real(request, repository)

@login_required()
def add_statements_real(request, repository):
    if request.method == 'POST':
        form = AddStatementsForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            content_type = f.content_type
            # if  the content type is "application/octet-stream" it's probably
            # django which didn't find the right one, try with "
            if content_type == "application/octet-stream":
                content_type = "text/plain"
                if f.name.endswith(".ttl"):
                    content_type = "text/turtle"
                elif f.name.endswith(".xml"):
                    content_type = "application/rdf+xml"
            ok, _, _, msg = add_repository_statements(repository, f, content_type,
                                                   True)
            if not ok:
                messages.add_message(request, messages.ERROR, msg)
            else:
                messages.add_message(request, messages.INFO,
                                     "Statements have been added")
                #edited_repository_signal.send(None, user=request.user, repository=repository)
            return redirect('triple_ui:view', repository=repository)
    else:
        form = AddStatementsForm()

    ctx = {
        "form": form,
        "repository": repository,
    }
    return render(request, 'triple_ui/add_statements.html', ctx)


@login_required()
def delete(request, repository):
    if request.method == "POST":
        ok, _, _, msg = delete_repository(repository)
        if not ok:
            messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request, messages.INFO,
                                 "The repository '{}' has been deleted".format(repository))
        #delete_repository_signal.send(None, user=request.user, repository=repository)
        return redirect('triple_ui:home')

    return render(request, 'triple_ui/delete_repo.html', {'repository': repository})



@login_required
def new(request):
#     # User must be able to create a repository ?
#     if not request.user.administrator:
#         raise PermissionDenied

    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            repository = data['name']
            ok, _, _, msg = create_repository(repository)
            if not ok:
                messages.add_message(request, messages.ERROR, msg)
            else:
                messages.add_message(request, messages.INFO,
                                 "The repository '{}' has been created".format(repository))
            #new_repository_signal.send(None, user=request.user, repository=repository)
            return redirect('triple_ui:view', repository=repository)
    else:
        form = RepositoryForm()

    ctx = {
        "form": form,
    }
    return render(request, 'triple_ui/new_repo.html', ctx)

