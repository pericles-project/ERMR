""""Listener UI views

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

from indigo.models import (
    Collection,
    ListenerLog
)



@login_required()
def home(request):
    collection = Collection.find("/scripts")
    _, child_dataobject = collection.get_child()
    
    full_logs = {}
    for script_name in child_dataobject:
        script_name = "/scripts/{}".format(script_name)
        full_logs[script_name] = ListenerLog.recent(script_name, 5)
    
    ctx = {"logs": full_logs}
    
    return render(request, 'listener/index.html', ctx)


