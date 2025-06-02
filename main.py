import io
import os
import time
import requests
import shutil
import tempfile
import zipfile
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from generate_ct_image import generate_nifti_file

load_dotenv()

app = Flask(__name__)
# CORS(app)
CORS(app, origins=["http://localhost:8000"])

@app.route('/generate_nifti', methods=['POST'])
def generate_nifti():
    print("Generating NIfTI file...")
    try:
        data = request.get_json()
        body_region = data.get('body_region')
        anatomy = data.get('anatomy')
        xy_dim = data.get('xy_dim')
        z_dim = data.get('z_dim')
        cor_sag_spacing = data.get('cor_sag_spacing')
        axial_spacing = data.get('axial_spacing')
        controllable_anatomy = data.get('controllable_anatomy')
        scale = data.get('scale')
        print(body_region, anatomy, xy_dim, z_dim, cor_sag_spacing, axial_spacing, controllable_anatomy, scale)
        output_path = generate_nifti_file(
            body_region, anatomy, xy_dim, z_dim, cor_sag_spacing, axial_spacing, controllable_anatomy, scale
        )
        return jsonify({'nifti_url': output_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nifti/<path:filename>')
def serve_nifti(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)


