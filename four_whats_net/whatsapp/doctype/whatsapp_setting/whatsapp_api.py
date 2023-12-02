import frappe
import requests
import base64
from PIL import Image
from io import BytesIO
import os
import uuid

@frappe.whitelist()
def initialise(url, key, token):
    url = url
    params = {
        'webhook': 'true',
        'key': key,
        'token': token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request successful")
        print(response.text)  # Displaying the response text
        return response.text
    else:
        print(f"Request failed with status code: {response.status_code}")
        return response.text


@frappe.whitelist()
def get_qrcode(url, key):
    url = url
    params = {
        'webhook': 'true',
        'key': key,
        # 'token': token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request successful")

        # Extracting Base64 data from the response JSON
        response_json = response.json()
        base64_data = response_json.get('qrcode', '')

        if isinstance(base64_data, str) and base64_data.startswith('data:image/png;base64,'):
            # Extracting image data from Base64 string
            base64_string = base64_data.split('base64,')[1]

            # Decode Base64 to bytes and create an image
            img_data = base64.b64decode(base64_string)
            img = Image.open(BytesIO(img_data))

            # Generate a random filename for the image
            filename = f"qr_code_{uuid.uuid4().hex}.png"

            # Specify the file path where the image will be saved
            file_path = f'/home/rsa/dev-bench/sites/dev.rsainfra.in/public/files/{filename}'

            # Saving the image to the specified file path
            img.save(file_path)
            print(f"Image saved as {filename} in /home/rsa/dev-bench/sites/dev.rsainfra.in/public/files/")

            # Return the file path of the saved image
            return file_path
        else:
            print("Invalid or missing Base64 image data")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

@frappe.whitelist()
def get_status(url, key):
    url = url
    params = {
        'webhook': 'true',
        'key': key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request successful")
        print(response.text)  # Displaying the response text
        return response.text
    else:
        print(f"Request failed with status code: {response.status_code}")
        return response.text