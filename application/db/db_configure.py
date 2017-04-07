
config = ConfigManager(defs.DB_CFG_PATH)


def _association_uri(server='mysql', user=None, password=None,
                     host=None, port=None, database=None):
    SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (server, user, password, host, port, database)
    return SQLALCHEMY_DATABASE_URI


def sqlalchemy_database_uri():
    sections = config.cp.sections()
    URI = None
    for section in sections:
        config.section = section

        user = config.get('user')
        password = config.get('password')
        host = config.get('host')
        port = config.get('port')
        database = config.get('database')

        URI = _association_uri(section, user, password, host, port, database)
    if not URI:
        raise exception.DBNotInit("database not init, can't connect to sql.")
    return URI


if __name__ == '__main__':
    sqlalchemy_database_uri()

