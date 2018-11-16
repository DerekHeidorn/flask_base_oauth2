import os
import unittest
import coverage
import argparse
from subprocess import Popen, PIPE
from project.app import main

parser = argparse.ArgumentParser()
parser.add_argument("command", choices=['test', 'coverage', 'runserver', 'emailserver'], help="Command Action")

args = parser.parse_args()


def setup_dev_settings():
    # for using http instead of https
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Application specific
    os.environ["APP_FLASK_SECRET_KEY"] = "wbr59q8tof3k2FfeSIvO"
    os.environ["APP_SECRET_KEY"] = "KlkdZyb5xrGpDcNkSBrDhe790ohLfuea"

    os.environ["APP_JWT_ISS"] = "https://localhost:9000"
    os.environ["APP_JWT_KEY"] = "BMcrqdcd7QeEmR8CXyU"

    # database config
    os.environ["APP_DB_CONNECTION_URI"] = "postgresql://postgres:P$F$xs+n?5+Ug3AU5PTe3q@localhost/postgres"
    os.environ["APP_DB_ENGINE_DEBUG"] = "False"


'''
Setting an SMTP server:
python -m smtpd -n -c DebuggingServer localhost:25
'''
def run_smtp_server():
    print("Hello")
    # smtpd_cmd = ["python", "-m", "smtpd", "-n", "-c", "DebuggingServer", "localhost:25"]
    # process = Popen(smtpd_cmd, stdout=PIPE)
    # (output, err) = process.communicate()
    # exit_code = process.wait()
    # print("called ffmpeg:" + str(exit_code))


def run_test():
    setup_dev_settings()
    app = main.create_application()

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


def run_coverage():
    setup_dev_settings()
    app = main.create_application()

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
        cov_dir = os.path.join(basedir, 'tmp/coverage')
        code_coverage.html_report(directory=cov_dir)
        print('HTML version: file://%s/index.html' % cov_dir)
        code_coverage.erase()
        return 0
    return 1


def run_dev_server():
    setup_dev_settings()
    app = main.create_application()
    options = {'use_debugger': False, 'threaded': True, 'use_reloader': False}
    app.run(debug=False, host="127.0.0.1", port=9000, **options)


# ----------------------
# --- Execute Type ---
# ----------------------

if args.command == 'runserver':
    run_dev_server()

elif args.command == 'test':
    run_test()

elif args.command == 'coverage':
    run_coverage()

elif args.command == 'emailserver':
    run_smtp_server()

# if __name__ == "__main__":
#     run_server()
