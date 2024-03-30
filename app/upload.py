import os
from functools import wraps

import cv2
from flask import jsonify, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_image(image_path, max_size=4 * 1024 * 1024, max_height=2048, scale_factor=0.9):
    """
    Resize the image using OpenCV to ensure it's under the maximum file size and height.
    """
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width = img.shape[:2]

    # Check and adjust the height first
    if height > max_height:
        aspect_ratio = width / height
        new_width = int(max_height * aspect_ratio)
        img = cv2.resize(img, (new_width, max_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(image_path, img)  # Write the resized image back

    # Now check and adjust the file size if necessary
    while os.path.getsize(image_path) > max_size and scale_factor > 0.1:
        # Re-read the image in case it was resized above
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        width = int(img.shape[1] * scale_factor)
        height = int(img.shape[0] * scale_factor)
        dim = (width, height)

        # Resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        # Overwrite the original image with the resized image
        cv2.imwrite(image_path, resized)
        scale_factor *= 0.9  # Reduce the scale factor for the next iteration if needed


def file_upload(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            # Resize the image if necessary using OpenCV
            resize_image(save_path)
            result = f(save_path, *args, **kwargs)

            # check file exits
            if os.path.exists(save_path):
                os.remove(save_path)

            return result
        else:
            return jsonify({'success': False, 'message': 'Invalid file type.'}), 400

    return decorated_function
