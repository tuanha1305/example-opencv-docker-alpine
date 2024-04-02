import os

import cv2
from flask import Blueprint, jsonify, request, current_app
from app.entity.map import MapSchema

from app.upload import file_upload

api_blueprint = Blueprint('api', __name__)


def error_handler(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ZeroDivisionError:
            return jsonify({"success": False, "message": "Division by zero is not allowed"}), 400
        except KeyError as e:
            message = f'An error occurred: {str(e)}' if current_app.debug else 'An internal error occurred. Please try again later.'
            return jsonify({"success": False, "message": message}), 400
        except Exception as e:
            message = f'An error occurred: {str(e)}' if current_app.debug else 'An internal error occurred. Please try again later.'
            return jsonify({"success": False, "message": message}), 500

    wrapper.__name__ = f.__name__
    return wrapper


@api_blueprint.route("/api/v1/health-check", methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'Success.'
    }), 200


@api_blueprint.route('/api/v1/size', methods=['POST'])
@file_upload
@error_handler
def get_size(save_path):
    try:
        img = cv2.imread(save_path)
        height, width, channels = img.shape
        size = os.path.getsize(save_path)

        result = {
            'width': width,
            'height': height,
            'size_bytes': size,
            'channels': channels
        }
        return jsonify({'success': True, 'data': result, 'message': 'Successfully uploaded.'}), 200

    except Exception as e:
        message = f'An error occurred: {str(e)}' if current_app.debug else 'An internal error occurred. Please try again later.'
        return jsonify({'success': False, 'message': message}), 500


@api_blueprint.route('/api/v1/map-preview', methods=['POST'])
@error_handler
def map_preview():
    try:
        payload = request.get_json()
        map_info = MapSchema()
        errors = map_info.validate(payload)

        if errors:
            return jsonify({'success': False, 'message': 'Validation error', 'errors': errors}), 400

        return jsonify({'success': True, 'data': payload, 'message': 'Successfully.'}), 200

    except Exception as e:
        message = f'An error occurred: {str(e)}' if current_app.debug else 'An internal error occurred. Please try again later.'
        return jsonify({'success': False, 'message': message}), 500
