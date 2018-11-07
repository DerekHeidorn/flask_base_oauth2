import os
import unittest
import coverage

from flask import Flask
from flask_script import Server, Manager
from project.app import main

# app = createApplication()
# manager = Manager(app)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTH_INSECURE_TRANSPORT'] = '1'
os.environ['DEBUG'] = '1'

app = main.createApplication()
manager = Manager(app)

#manager = Manager()
# manager.add_command("runserver", Server(host="0.0.0.0", port=9000))

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

'''
python -m unittest project/tests/web/testCommon.py
'''
@manager.command
def test():
    """Runs the unit tests without test coverage."""
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

    

    #for k in sorted(os.environ.keys()):
    #    print(k + ":" + os.environ[k])

    #application = main.createApplication()
    options = {'use_debugger':True, 'threaded':False, 'use_reloader':True}
    app.run(debug=False, host="127.0.0.1", port=9000, **options)

#     # ptvsd.enable_attach(secret="my_secret", address=('0.0.0.0', 3000))







if __name__ == "__main__":
    manager.run()