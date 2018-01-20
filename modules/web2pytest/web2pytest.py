# -*- coding: utf-8 -*-

"""Infrastructure to run an Web2py application under test environment.
We create a temporary file to indicate the application she's running
under test.
By default this file is created in ramdisk (Ubuntu) to speed up
execution.
Web2py applications need this external injection mainly to know
where to create their test database.
"""

import os

# __all__ = ['delete_testfile', 'create_testfile', 'is_running_under_test']

# default_path = "/tmp"
default_path = "/dev/shm/web2py_test"  # native ramdisk is faster
default_filename = "web2py_test_indicator"

_test_filename = None

WEB2PY_ENV = "WEB2PY_ENV"
WEB2PY_TEST_ENV = "TEST"

def set_test_environment(environment):
    environment[WEB2PY_ENV] = WEB2PY_TEST_ENV

def close_test_environment(environment):
    environment[WEB2PY_ENV] = ""

def is_test_environment():
    try:
        is_test_environment = os.environ[WEB2PY_ENV] == WEB2PY_TEST_ENV
    except:
        is_test_environment = False
    return is_test_environment
