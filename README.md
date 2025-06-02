# 3D CT Medical Imagery

A modern web app for generating and viewing synthetic 3D CT medical images, powered by AMD GPU Droplets and DigitalOcean App Platform.

## Features
- Select body region and anatomical structures to generate synthetic CT images
- Adjustable resolution and output spacing
- Interactive 3D NIfTI viewer in the browser
- Clean, DigitalOcean-inspired UI

## Technologies Used
- Python (Flask) backend
- JavaScript, HTML, CSS frontend
- Niivue for NIfTI visualization
- DigitalOcean App Platform (for deployment)
- AMD GPU Droplets (for compute)

## Setup Instructions

### 1. Backend (Flask)
- Install Python 3.8+
- Install dependencies:
  ```bash
  pip install flask flask-cors requests python-dotenv nibabel numpy matplotlib
  ```
- Run the backend:
  ```bash
  python main.py
  ```
- The backend will be available at `http://127.0.0.1:5000/`

### 2. Frontend
- Open `index.html` in your browser (or serve with any static file server)
- Make sure the backend is running and accessible

### 3. DigitalOcean Deployment
- Deploy the backend as a DigitalOcean App (Python/Flask)
- Deploy the frontend as a static site (or serve from the same Flask app)
- Use AMD GPU Droplets for compute if needed

## Usage
1. Select a body region and anatomy
2. Adjust resolution and spacing as needed
3. Click Submit to generate and view the synthetic CT image
4. Use the viewer to explore the generated NIfTI file

## License
[Add your license here] 