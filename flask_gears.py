import mimetypes
import os
from StringIO import StringIO
from flask import send_file

from gears.assets import build_asset
from gears.environment import Environment
from gears.exceptions import FileNotFound
from gears.finders import FileSystemFinder


class Gears(object):

    def __init__(self, app=None, defaults=True, assets_folder='assets'):
        self.defaults = defaults
        self.assets_folder = assets_folder
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app
        self.init_environment()
        self.replace_static_view()

    def init_environment(self):
        self.environment = Environment(self.get_static_folder())
        if self.defaults:
            self.environment.register_defaults()
            self.environment.finders.register(self.get_default_finder())

    def replace_static_view(self):
        self.original_static_view = self.app.view_functions['static']
        self.app.add_url_rule(self.app.static_url_path + '/<path:filename>',
                              endpoint='static', view_func=self.send_asset)

    def send_asset(self, filename):
        try:
            asset = build_asset(self.environment, filename)
        except FileNotFound:
            return self.original_static_view(filename)
        mimetype, encoding = mimetypes.guess_type(filename)
        return send_file(StringIO(asset), mimetype=mimetype, conditional=True)

    def get_default_finder(self):
        return FileSystemFinder(directories=(self.get_assets_folder(),))

    def get_static_folder(self):
        return self.app.static_folder

    def get_assets_folder(self):
        return os.path.join(self.app.root_path, self.assets_folder)
