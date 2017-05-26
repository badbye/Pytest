# encoding: utf8

"""
Created on 2017.01.06

@author: yalei
"""

from utils import test_numpy_array, test_df, test_list
import tornado.web
import tornado.ioloop
import tornado.autoreload
from tornado.web import StaticFileHandler
from tornado.options import define, options
import sys
import os


define('port', default=9009, help='port')
TEST_CLASS = {
    'DataFrame': test_df,
    'array': test_numpy_array,
    'list': test_list
}


class TestHandle(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.redirect('static/index.html')

    def post(self, code='', name='', obj=''):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        code = self.get_argument('code', '').encode('utf-8')
        name = self.get_argument('name', '').encode('utf-8')
        obj = self.get_argument('class').encode('utf-8')
        if obj not in TEST_CLASS:
            self.finish({'error': True, 'msg': '"class" should be in %s' % TEST_CLASS.keys()})
            return
        try:
            d = {f.__name__: f for f in TEST_CLASS.values()}
            exec(code, d, d)
            self.finish({'error': False, 'code': TEST_CLASS[obj](name, d[name])})
            del d
        except Exception as e:
            s = sys.exc_info()
            self.finish({'error': True, 'msg': '%s; line[%s]' % (s[1], s[2].tb_lineno)})


MORE_SETTINGS = {
    "cookie_secret": "698EsDMXqAgaSddK8gFGGeDJFuts0EQnp3XdTP9o/Vo=",
    "static_path": os.path.join(os.path.dirname(__file__), 'static'),
    # "xsrf_cookies": True,
}


def make_app():
    return tornado.web.Application([
        (r"/", TestHandle),
        (r"/static", StaticFileHandler, {'path': MORE_SETTINGS['static_path'], 'default_filename': 'index.html'}),
    ], **MORE_SETTINGS)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    port = int(options.port)
    app = make_app()
    app.listen(port)
    tornado.autoreload.watch(os.path.join(os.path.dirname(__file__), 'static/index.html'))
    tornado.autoreload.start()
    print('Server: http://0.0.0.0:%s' % port)
    tornado.ioloop.IOLoop.current().start()
