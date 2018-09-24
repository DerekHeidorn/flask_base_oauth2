
from flask import Flask
from flask_script import Server, Manager
from web.app import createApplication

# app = createApplication()
# manager = Manager(app)

app = Flask(__name__)

manager = Manager(app)
# manager.add_command("runserver", Server(host="0.0.0.0", port=9000))

@manager.command
def runserver():
    # apiApplication = createApplication()
    # Server(host="127.0.0.1", port=9000)
    # apiApplication.run()

    apiApplication = createApplication()
    options = {'use_debugger':True, 'threaded':False, 'use_reloader':True}
    apiApplication.run(debug=False, host="127.0.0.1", port=9000, **options)

#     # ptvsd.enable_attach(secret="my_secret", address=('0.0.0.0', 3000))



#     # print('ptvsd is started')
#     # options = {'use_debugger':True, 'threaded':False, 'use_reloader':True}
#     # manager.run(debug=False, host="0.0.0.0", port=5000, **options)
#     manager.run()


@manager.command
def hello():
    print("hello")

if __name__ == "__main__":
    manager.run()