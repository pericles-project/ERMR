"""

Copyright 2015 Archive Analytics Solutions - University of Liverpool

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


from indigo.models import User

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def administrator_required(function=None,
                           redirect_field_name=REDIRECT_FIELD_NAME,
                           login_url=None):
    """
    Decorator for views that checks that the user is logged in and an
    administrator
    """
    actual_decorator = user_passes_test(
        lambda u: u.administrator,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

class Backend(object):

    def get_user(self, id):
        return User.find(username)

    def authenticate(self, username=None, password=None):
        user = User.find(username)
        if not user:
            print "User not found"
            return None
        if not user.authenticate(password):
            print "User not authenticated"
            return None
        return user
