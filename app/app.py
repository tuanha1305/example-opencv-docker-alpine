import logging
import time
from flask import Flask, g, request, jsonify, current_app
from time import strftime

from app.routes import api_blueprint
from app.upload import UPLOAD_FOLDER
from flask_cors import CORS


class App:
    def __init__(self, cfg):
        self.http_server = Flask(__name__)
        CORS(self.http_server)
        app_config = cfg.get('app')
        self.port = app_config.get('port')
        self.debug = app_config.get('debug')

        # set current_app ptr, s3 & debug
        self.configure_app()

        # config upload folder
        self.http_server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        self.register_before_after_request()
        self.register_routes()

    def run(self):
        self.http_server.run(host='0.0.0.0', port=self.port, debug=self.debug)

    def register_before_after_request(self):
        @self.http_server.before_request
        def _before_request():
            g.start = time.time()

        @self.http_server.after_request
        def _after_request(response):
            timestamp = strftime('[%Y-%b-%d %H:%M]')
            diff = time.time() - g.start
            logging.info('%s %s %s %s %s %s %.2f', timestamp, request.remote_addr, request.method, request.scheme,
                         request.full_path, response.status, diff)

            return response

        @self.http_server.errorhandler(404)
        def page_not_found(e):
            return jsonify({
                'success': False,
                'message': f"Not found. {e if self.debug else ''}"
            }), 404

        @self.http_server.errorhandler(405)
        def method_not_allowed(e):
            return jsonify({
                'success': False,
                'message': "Method not allowed." + (f" {e}" if self.debug else "")
            }), 405

        @self.http_server.errorhandler(500)
        def internal_server_error(e):
            return jsonify({
                'success': False,
                'message': f"Internal server error. {e if self.debug else ''}"
            }), 500

    def register_routes(self):
        self.http_server.register_blueprint(api_blueprint)

    def configure_app(self):
        with self.http_server.app_context():
            current_app.debug = self.debug
