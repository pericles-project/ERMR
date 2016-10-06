"""unittest class for utility package 

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


import unittest
import StringIO

from indigo.metadata import (MetadataValidator,
                             get_resource_validator,
                             get_collection_validator)

from nose.tools import raises

TEST_RULES = [
    {
        "name": "required-field",
        "required": True,
    },
    {
        "name": "required-choice",
        "required": True,
        "choices": ["a", "b"] # Non-optional constrained choices
    },
    {
        "name": "non-required-choice",
        "required": False,
        "choices": ["a", "b"] # Optional constrained choices
    },
]

def rules_as_fileobj():
    import json

    return StringIO.StringIO(json.dumps({"resources":TEST_RULES, "collections":TEST_RULES}))

class MetadataValidationTest(unittest.TestCase):
    _multiprocess_can_split_ = True

    def test_validation_empty(self):
        m = MetadataValidator([])
        ok, errs = m.validate({})
        assert ok == True
        assert errs == []

    def test_validation_empty_rules(self):
        m = MetadataValidator([])
        ok, errs = m.validate({"field": "value"})
        assert ok == True
        assert errs == []

    def test_validation_empty_input(self):
        m = get_resource_validator(rules_as_fileobj())
        ok, errs = m.validate({})
        assert ok == True
        assert errs == []

    def test_failing_requires(self):
        m = get_resource_validator(rules_as_fileobj())
        ok, errs = m.validate({"required-field": ""})
        assert ok == False
        assert len(errs) == 1

    def test_failing_choice(self):
        m = get_resource_validator(rules_as_fileobj())
        ok, errs = m.validate({"required-choice": "z"})
        assert ok == False
        assert len(errs) == 1

    def test_failing_choice_empty(self):
        m = get_resource_validator(rules_as_fileobj())
        ok, errs = m.validate({"required-choice": ""})
        assert ok == False
        assert len(errs) == 1

    def test_failing_non_required_choice(self):
        m = get_resource_validator(rules_as_fileobj())
        ok, errs = m.validate({"non-required-choice": "z"})
        assert ok == False
        assert len(errs) == 1

    def test_failing_non_required_choice_empty(self):
        m = get_resource_validator(rules_as_fileobj())
        ok, errs = m.validate({"non-required-choice": ""})
        assert ok == True
        assert len(errs) == 0

