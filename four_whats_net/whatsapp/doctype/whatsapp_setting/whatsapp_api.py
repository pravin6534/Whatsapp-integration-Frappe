import frappe
import requests
import base64
from PIL import Image
from io import BytesIO
import os
import uuid
import urllib.parse

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
        
            # Encode the Base64 string to be URL-safe
            encoded_data = base64_string.replace('+', '-').replace('/', '_').rstrip('=')

            # Construct the URL-encoded data
            encoded_data_url = urllib.parse.quote(encoded_data, safe='')

            # Generate the QR code link using the API endpoint and the encoded URL component
            file_path = base64_data
          
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
