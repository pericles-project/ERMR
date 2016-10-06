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


from . import views

urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^view/(?P<repository>.*)$', views.view, name='view'),
   
    url(r'^new/repository$', views.new, name='new_repository'),
    url(r'^delete/repository/(?P<repository>.*)$', views.delete, name='delete_repository'),
    url(r'^delete/statements/(?P<repository>.*)$', views.delete_statements, name='delete_statements'),
    url(r'^add/repository/(?P<repository>.*)$', views.add_statements, name='add_statements'),
   
]
