#!/usr/bin/env python

''' py.test configuration and fixtures file.
Tells application she's running in a test environment.
Creates a complete web2py environment, similar to web2py shell.
Creates a WebClient instance to browse your application, similar to a real
web browser.
Propagates some application data to test cases via fixtures, like baseurl and
automatic appname discovering.
'''

import os
import shutil
import signal
import subprocess
import urllib
from time import sleep

import pytest
import sys

from applications.journalmanagement.modules.web2pytest import web2pytest

sys.path.insert(0, '')
WEB2PY_TEST_PORT = 8081

def pytest_namespace():
    return {'web2py_process': None,
            'web2py_environment': None
            }

def get_web2py_path():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    a = tests_dir.split("/")
    return "/".join(a[:-3])

@pytest.fixture(scope='session')
def appname():
    '''Discover application name.
    Your test scripts must be on applications/<your_app>/tests
    '''

    dirs = os.path.split(__file__)[0]
    appname = dirs.split(os.path.sep)[-2]
    # sys.path.insert(1, os.path.join(os.getcwd(), 'applications', appname))
    return appname

TEST_DB_DIR = os.path.join(get_web2py_path(), "applications", appname(), "databases", "test")

@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:

    pytest.web2py_environment = os.environ.copy()

    web2pytest.set_test_environment(pytest.web2py_environment)

    print ("akak1",TEST_DB_DIR)
    if not os.path.exists(TEST_DB_DIR):
        os.makedirs(TEST_DB_DIR)

    cmd = "python3 {web2py_executable} -i localhost --nogui --debug=0 -p {port} -a 'supersekret' &> web2py.log &".format(
        web2py_executable=os.path.join(get_web2py_path(), "web2py.py"),
        port=WEB2PY_TEST_PORT
    )

    pytest.web2py_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid, env=pytest.web2py_environment)
    sleep(5)
    # request for populate DB and avoid sqlite errors
    with urllib.request.urlopen(baseurl(appname())) as response:
        response.read()

def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    os.killpg(os.getpgid(pytest.web2py_process.pid), signal.SIGTERM)
    web2pytest.close_test_environment(pytest.web2py_environment)
    if os.path.exists(TEST_DB_DIR):
        shutil.rmtree(TEST_DB_DIR)

@pytest.fixture(scope='session')
def baseurl(appname):
    '''The base url to call your application.
    Change you port number as necessary.
    '''

    return 'http://localhost:%s/%s' % (WEB2PY_TEST_PORT, appname)




@pytest.fixture(scope='session', autouse=True)
def create_database(web2py):
    # import testdb
    db = web2py.db
    # testdb.fill_tables(db)


# @pytest.fixture(autouse=True)
# def cleanup_db(web2py):
#     '''Truncate all database tables before every single test case.
#
#     This can really slow down your tests. So, keep your test data small and try
#     to allocate your database in memory.
#
#     Automatically called by test.py due to decorator.
#     '''
#     web2py.db.rollback()
#     for tab in web2py.db.tables:
#         web2py.db[tab].truncate()
#     web2py.db.commit()


@pytest.fixture(scope='session')
def client(baseurl):
    '''Create a new WebClient instance once per session.
    '''

    from gluon.contrib.webclient import WebClient
    webclient = WebClient(baseurl)
    return webclient


# @pytest.fixture()
@pytest.fixture(scope='session')
def web2py(appname):
    '''Create a Web2py environment similar to that achieved by
    Web2py shell.
    It allows you to use global Web2py objects like db, request, response,
    session, etc.
    Concerning tests, it is usually used to check if your database is an
    expected state, avoiding creating controllers and functions to help
    tests.
    '''

    def run(controller, function, env):
        """Injects request.controller and request.function into
        web2py environment.
        """

        from gluon.compileapp import run_controller_in

        env.request.controller = controller
        env.request.function = function

        r = None
        try:
            r = run_controller_in(controller, function, env)
        except HTTP as e:
            if str(e.status).startswith("2") or str(e.status).startswith("3"):
                env.db.commit()
            raise
        else:
            env.db.commit()
        finally:
            env.db.rollback()
        return r

    def submit(controller, action, env, data=None, formname=None):
        """Submits a form, setting _formkey and _formname accordingly.
        env must be the web2py environment fixture.
        """

        formname = formname or "default"

        hidden = dict(
            _formkey=action,
            _formname=formname
        )
        if data:
            env.request.post_vars.update(data)

        env.request.post_vars.update(hidden)
        env.session["_formkey[%s]" % formname] = [action]

        return env.run(controller, action, env)

    def send(controller, action, env, data=None):
        """Call a controller action using get.
        env must be the web2py environment fixture.
        data must be a dictionary with the request args
        """
        if data:
            env.request.vars.update(Storage(data))

        return env.run(controller, action, env)

    from gluon.shell import env
    from gluon.storage import Storage
    web2py_env = env(appname, import_models=True,
                     extra_request=dict(is_local=True,
                                        _running_under_test=True))

    if '__file__' in web2py_env:
        del web2py_env['__file__']  # avoid py.test import error
    web2py_env['run'] = run
    web2py_env['send'] = send
    web2py_env['submit'] = submit
    globals().update(web2py_env)

    return Storage(web2py_env)