import requests
import frappe


@frappe.whitelist()
def sendmsg(url,key,contact,message):
    try:
        # Maytapi API key
        maytapi_key = key

        # Recipient's phone number
        to_number = contact  # Replace with the recipient's phone number

        # Payload for the API request
        payload = {
            "to_number": to_number,
            "type": "text",
            "message": message
        }

        headers = {
            'x-maytapi-key': maytapi_key,
            'content-type': "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        result = {'message': 'Operation completed successfully '}
        frappe.msgprint("sucess")
    except Exception as e:
        print(str(e))