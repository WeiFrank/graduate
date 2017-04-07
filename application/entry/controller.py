from application.apps import create_app
from application.db.session import init_db_session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell

def main(port=27000):
    app, db = create_app()
    init_db_session(db)
    #migrate = Migrate(app, db)
    #manager = Manager(app)
    #print "Listening http://0.0.0.0:%s/" % port
    # if is_log:
    #     app.wsgi_app = MyWsgiLog(app.wsgi_app)

    app.run(host="0.0.0.0", port=port)

def debug():

    app, db = create_app()
    print  'ttttttttttttttt' , db
    init_db_session(db)
    migrate = Migrate(app, db)
    manager = Manager(app)



    def make_shell_context():
        return dict(app=app, db=db)

    manager.add_command('db', MigrateCommand)
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command("runserver", Server(host="0.0.0.0", port=27000, use_debugger=True, use_reloader=True))

    manager.run()
if __name__ == '__main__':
    main()