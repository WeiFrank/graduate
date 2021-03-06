import  os
class render_jinja:
    """Rendering interface to Jinja2 Templates

    Example:

        render= render_jinja('templates')
        render.hello(name='jinja2')
    """

    def __init__(self, *a, **kwargs):
        a = (os.path.join(pwd_path, a[0]),) + a[1:-1]
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        from jinja2 import Environment, FileSystemLoader
        self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)

    def __getattr__(self, name):
        # Assuming all templates end with .html
        path = name + '.html'
        t = self._lookup.get_template(path)
        self.set_render_globals()
        return t.render

    def set_render_globals(self):
        self._lookup.globals.update(_=_)
        self._lookup.globals.update(is_fusionnas=is_fusionnas)
        self._lookup.globals.update(session=session)
        self._lookup.globals.update(config=config)
        self._lookup.globals.update(check_permission=db_api.check_permission)
        self._lookup.globals.update(http_host=get_http_host())