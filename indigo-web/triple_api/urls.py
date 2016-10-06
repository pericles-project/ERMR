""""Fact URLs

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

from django.conf.urls import (
    url,
    include
)
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
   url(r'^(?P<repository>\w+)/statements$', views.statements, name="statements"),
   url(r'^(?P<repository>\w+)$', views.repository, name="repository"),
   url(r'^$', views.ls_repositories, name="ls_repositories"),
   
   url(r'^(?P<repository>\w+)/dependency$', views.dependency, name="dependency"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


