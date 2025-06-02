import io
import os
import time
import requests
import shutil
import tempfile
import zipfile
from dotenv import load_dotenv

load_dotenv()

def generate_nifti_file(body_region, anatomy, xy_dim, z_dim, cor_sag_spacing, axial_spacing, controllable_anatomy, scale):
    invoke_url = "https://health.api.nvidia.com/v1/medicalimaging/nvidia/maisi"
    fetch_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"
    headers = {
        "Authorization": "Bearer " + os.getenv("NVIDIA_API_TOKEN"),
        "Accept": "application/json",
        "content_type_header": "Content-Type: application/json"
    }

    # Convert to correct types if needed
    if isinstance(body_region, list):
        body_region_list = body_region
    else:
        body_region_list = [body_region]
    if isinstance(anatomy, list):
        anatomy_list = anatomy
    else:
        anatomy_list = [anatomy]
    output_size = [int(xy_dim), int(xy_dim), int(z_dim)]
    spacing = [float(cor_sag_spacing), float(cor_sag_spacing), float(axial_spacing)]
    controllable_anatomy_size = []
    if controllable_anatomy and scale:
        try:
            controllable_anatomy_size = [[controllable_anatomy, float(scale)]]
        except Exception:
            controllable_anatomy_size = []

    os.makedirs("images", exist_ok=True)
    result = "images/" + "result_" + str(body_region_list) + "_" + str(anatomy_list) + "_" + str(time.time())
    payload = {
        "num_output_samples": 1,
        "body_region": body_region_list,
        "anatomy_list": anatomy_list,
        "controllable_anatomy_size": controllable_anatomy_size,
        "output_size": output_size,
        "image_output_ext": ".nii.gz",
        "label_output_ext": ".nii.gz",
        "pre_signed_url": "",
        "spacing": spacing,
    }
    print(payload)

    session = requests.Session()
    try:
        response = session.post(invoke_url, headers=headers, json=payload)
        try:
            print(response.json())
        except Exception:
            print("Response is not JSON:", response.content)
        response.raise_for_status()
        while response.status_code == 202:
            req_id = response.headers.get("NVCF-REQID")
            req_url = os.path.join(fetch_url, req_id)
            response = session.get(req_url, headers=headers)
            print(f"Please wait util response returned...")
            time.sleep(1)
    except Exception as e:
        print("Error during API call:", e)
        if 'response' in locals():
            try:
                # print("Response content:", response.content)
                print("Exception:", e)
            except Exception:
                pass
        raise

    z = zipfile.ZipFile(io.BytesIO(response.content))
    os.makedirs(result, exist_ok=True)
    z.extractall(result)

    for root, dirs, files in os.walk(result):
        for fname in files:
            if fname.startswith('sample') and fname.endswith('image.nii.gz'):
                return result + "/" + fname

    raise FileNotFoundError("No file starting with 'sample' and ending with 'image.nii.gz' found in the extracted results.")


# if response.status_code != 200:
#     print(f"Error with code {response.status_code}.")
#     exit()

# with tempfile.TemporaryDirectory() as temp_dir:
#     z = zipfile.ZipFile(io.BytesIO(response.content))
#     z.extractall(temp_dir)
#     os.makedirs(result)
#     shutil.move(temp_dir, f"{result}")

# print("Success!")
