from flask_script import Manager
from web import createApplication

app = createApplication()
manager = Manager(app)

@manager.command
def runserver():
    # ptvsd.enable_attach(secret="my_secret", address=('0.0.0.0', 3000))
    print('ptvsd is started')
    options = {'use_debugger':True, 'threaded':False, 'use_reloader':True}
    app.run(debug=False, host="0.0.0.0", port=5000, **options)


