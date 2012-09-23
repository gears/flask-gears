import mimetypes
import os
from StringIO import StringIO
from flask import send_file, current_app

from gears.assets import build_asset
from gears.environment import Environment, DEFAULT_PUBLIC_ASSETS
from gears.exceptions import FileNotFound
from gears.finders import FileSystemFinder


class Gears(object):

    def __init__(self, app=None, defaults=True, assets_folder='assets',
                 compilers=None, compressors=None, public_assets=None,
                 cache=None):
        self.defaults = defaults
        self.assets_folder = assets_folder
        self.compilers = compilers
        self.compressors = compressors
        self.public_assets = public_assets
        self.cache = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['gears'] = {}
        self.init_environment(app)
        self.init_asset_view(app)

    def init_environment(self, app):
        environment = Environment(
            root=self.get_static_folder(app),
            public_assets=self.get_public_assets(app),
            cache=self.get_cache(app),
        )
        if self.defaults:
            environment.register_defaults()
            environment.finders.register(self.get_default_finder(app))
        if self.compilers is not None:
            for extension, compiler in self.compilers.items():
                environment.compilers.register(extension, compiler)
        if self.compressors is not None:
            for mimetype, compressor in self.compressors.items():
                environment.compressors.register(mimetype, compressor)
        app.extensions['gears']['environment'] = environment

    def init_asset_view(self, app):
        app.extensions['gears']['static_view'] = app.view_functions['static']
        app.add_url_rule(app.static_url_path + '/<path:filename>',
                         endpoint='static', view_func=self.asset_view)

    def asset_view(self, filename):
        environment = current_app.extensions['gears']['environment']
        static_view = current_app.extensions['gears']['static_view']
        try:
            asset = build_asset(environment, filename)
        except FileNotFound:
            return static_view(filename)
        mimetype, encoding = mimetypes.guess_type(filename)
        return send_file(StringIO(asset), mimetype=mimetype, conditional=True)

    def get_environment(self, app):
        return app.extensions['gears']['environment']

    def get_default_finder(self, app):
        return FileSystemFinder(directories=(self.get_assets_folder(app),))

    def get_static_folder(self, app):
        return app.config.get('GEARS_ROOT', app.static_folder)

    def get_assets_folder(self, app):
        return os.path.join(app.root_path, self.assets_folder)

    def get_public_assets(self, app):
        if self.public_assets is None:
            return DEFAULT_PUBLIC_ASSETS
        return self.public_assets

    def get_cache(self, app):
        return self.cache
