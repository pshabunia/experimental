#!/usr/bin/env python

import functions_framework
from flask import request, flash, redirect
from werkzeug.utils import secure_filename
from google.cloud import vision
import io
import os

@functions_framework.http
def handle(request):
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        try:
            sfilename = secure_filename(file.filename)
            filename = os.path.join('/tmp', sfilename)
            file.save(filename)
            print('original filename: "{}"'.format(file.filename))
            print('sanitized filename: "{}"'.format(sfilename))
            print('persisted filename: "{}"'.format(filename))
            return detect_document(filename)
        except Exception as err:
            return '{}'.format(err)
    # Render the form
    return """<html>
    <title>OCR Demo</title>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" />
        <input type="submit" value="upload" />
    </form>
    </html>"""

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception('{}'.format(response.error.message))
    return response.full_text_annotation.text
