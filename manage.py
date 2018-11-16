import os
import unittest
import coverage

from flask_script import Manager
from project.app import main
'''
Setting an SMTP server:
python -m smtpd -n -c DebuggingServer localhost:25
'''


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTH_INSECURE_TRANSPORT'] = '1'
os.environ['DEBUG'] = '1'

app = main.create_application()
manager = Manager(app)




@manager.command
def test():
    """Runs the unit tests without test coverage."""
    '''
    other examples: 
       python -m unittest project/tests/web/testCommon.py
       python -m unittest project.tests.web.testUsers.UserWebTestCase.test_reset_password
    '''
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    code_coverage = coverage.coverage(
        branch=True,
        include='project/*',
        omit=[
            'project/tests/*',
            'project/app/config.py',
            'project/app/*/__init__.py'
        ]
    )
    code_coverage.start()

    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests/web', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        code_coverage.stop()
        code_coverage.save()
        print('Coverage Summary:')
        code_coverage.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        code_coverage.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        code_coverage.erase()
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
