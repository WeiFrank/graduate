from application.apps import create_app
from application.db import models
from application.db.session import init_db_session
import argparse
import textwrap
from application.utils.exec_cmd import _exec_pipe
teacher_dict = {
       'name': 'professor',
       'number': 10,
}


class InitDbShell(object):
    def __init__(self):
        # self.install_path = utils.install_path
        # self.db_cfg_path = defs.DB_CFG_PATH
        pass
    def get_parser(self):
        parser = argparse.ArgumentParser(
            prog='InitTsstDatabase',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent("""
            +------------------------------------------------------------------+
            |    Initialization Ump database                                   |
            |    Automatically create the database configuration file          |
            |                            |
            |                                                                  |
            |    ump-initdb sqlite -n /var/mydatabase.db                       |
            |                                                                  |
            |    ump-initdb mysql -u root -p root -d ump                       |
            |                                                                  |
            +------------------------------------------------------------------+
            """ )
            #            add_help=False,
        )

        subparsers = parser.add_subparsers(dest='subcommand', metavar='<subcommand>')

        sqlite_parser = subparsers.add_parser('sqlite', help='use sqlite database')
        sqlite_parser.add_argument('-n', '--name',
                                   metavar='<name>',
                                   required=True,
                                   help='Select the sqlite database location.')

        mysql_parser = subparsers.add_parser('mysql', help='use mysql database')
        mysql_parser.add_argument('-u', '--user',
                                  metavar='<user>',
                                  required=True,
                                  help='mysql user name')
        mysql_parser.add_argument('-p', '--password',
                                  nargs="?",
                                  metavar='<password>',
                                  help='mysql password')
        mysql_parser.add_argument('-d', '--database',
                                  metavar='<database>',
                                  required=True,
                                  help='mysql database')
        mysql_parser.add_argument('--host',
                                  metavar='<host>',
                                  default='127.0.0.1',
                                  help='mysql host')
        mysql_parser.add_argument('--port', type=int,
                                  metavar='<port>',
                                  default=3306,
                                  help='mysql port')

        return parser

    def get_args(self):
        argv = sys.argv[1:]
        parser = self.get_parser()
        if argv == []:
            parser.print_help()

        args = parser.parse_args(argv)

    def main(self, args=None):
        if args is None:
            args = self.get_args()
        # print  'sssssssssss' ,args.subcommand
        # if args.subcommand == 'mysql' or args.server == 'mysql':
        #     db_cfg_kw['user'] = args.user
        #     db_cfg_kw['password'] = password
        #     db_cfg_kw['database'] = args.database
        #     db_cfg_kw['host'] = args.host
        #     db_cfg_kw['port'] = args.port
        #     db_cfg_kw['server'] = 'mysql'
        # return args



def init_teacher_role(role_name, number):
    role = models.TeacherRole.query.filter_by(name=role_name)
    if not role:
        values = {
            'username': role_name,
            'email': number,
        }
        role = models.TeacherRole(values).save()
    return role


def register_models():

    app, db = create_app()
    print  'iiiiiiiiiiiii' , db
    with app.app_context():
        db.create_all()

        #user = models.User('ZHUWEI', 'eee@11.com')
        #db.session.add(user)
        init_db_session(db)
        values = {'score':100}
        s = models.Grade(values).save()
        #
        # c = models.Student(values).save()
        v = {'student_num':'2013131018', 'change_num':12}
        #sub = models.Xuejichange(v).save()


def migrate_database():
    os.chdir('/root/PycharmProjects/tsst/entry/')
    print 'dddddddddddddd', os.curdir
    _exec_pipe("python %s db  init" % 'controller.py')
    _exec_pipe("python %s db migrate" % 'controller.py')
    cmd = "python %s db upgrade" % 'controller.py'
    _exec_pipe(cmd, is_raise=True)
    print "Database was upgraded sucessfully!"




if __name__ == '__main__':
    # InitDbShell().main()
    register_models()
    #migrate_database()