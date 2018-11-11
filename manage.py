import os
import unittest
import coverage

from flask_script import Manager
from project.app import main

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTH_INSECURE_TRANSPORT'] = '1'
os.environ['DEBUG'] = '1'

app = main.create_application()
manager = Manager(app)

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/app/config.py',
        'project/app/*/__init__.py'
    ]
)
COV.start()


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    '''
    other examples: python -m unittest project/tests/web/testCommon.py
    '''
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests/web', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def runserver():

    # apiApplication = createApplication()
    # Server(host="127.0.0.1", port=9000)
    # apiApplication.run()
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTH_INSECURE_TRANSPORT'] = '1'
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    os.environ['DEBUG'] = '1'
    os.environ['FLASK_DEBUG'] = '1'

    # for k in sorted(os.environ.keys()):
    #    print(k + ":" + os.environ[k])
    options = {'use_debugger': False, 'threaded': True, 'use_reloader': True}
    app.run(debug=False, host="127.0.0.1", port=9000, **options)


if __name__ == "__main__":
    manager.run()
