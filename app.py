# coding=utf-8
from __future__ import print_function
from collections import defaultdict

import web
from web import form
import config
import numbers

VERSION = "0.0.1"

urls = (
    r'/', 'Index',
    r'/about', 'About'
    )

app = web.application(urls, globals())

# Allow session to be reloadable in development mode.
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
                                  initializer={'flash': defaultdict(list)})

    web.config._session = session
else:
    session = web.config._session


def flash(group, message):
    session.flash[group].append(message)


def flash_messages(group=None):
    if not hasattr(web.ctx, 'flash'):
        web.ctx.flash = session.flash
        session.flash = defaultdict(list)
    if group:
        return web.ctx.flash.get(group, [])
    else:
        return web.ctx.flash

render = web.template.render('templates/',
                             base='base',
                             cache=config.cache)
t_globals = web.template.Template.globals
t_globals['datestr'] = web.datestr
t_globals['app_version'] = lambda: VERSION + ' - ' + config.env
t_globals['flash_messages'] = flash_messages
t_globals['render'] = lambda t, *args: render._template(t)(*args)


class Index:
    def GET(self):
        flash("success", """欢迎使用！可以单独翻译，也可批量翻译，批量翻译时注意一行一个数""")
        return render.index()

    def POST(self):
        number_service = numbers.NumberService()
        data = web.input()
        number = data.get('translate_input')
        num_list = number.split('\n')
        output_string = ''
        for item in num_list:
            item = item.strip()
            if item == '':
                continue
            result = number_service.parse_numer(int(item))
            output_string = output_string + result + '\n'
        return output_string


class About:
    def GET(self):
        return render.about()


# Set a custom internal error message
def internalerror():
    msg = """
    An internal server error occurred. Please try your request again by
    hitting back on your web browser. You can also <a href="/"> go back
     to the main page.</a>
    """
    return web.internalerror(msg)


# Setup the application's error handler
app.internalerror = web.debugerror if web.config.debug else internalerror

if config.email_errors.to_address:
    app.internalerror = web.emailerrors(config.email_errors.to_address,
                                        app.internalerror,
                                        config.email_errors.from_address)


# Adds a wsgi callable for uwsgi
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
