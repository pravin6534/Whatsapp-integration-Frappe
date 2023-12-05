import frappe
from frappe import _
from frappe.email.doctype.notification.notification import Notification, get_context, json
import requests

class ERPGulfNotification(Notification):
    
    def validate(self):
        self.validate_four_whats_settings()
        super(ERPGulfNotification, self).validate()
    
    def validate_four_whats_settings(self):
        settings = frappe.get_doc("Four Whats Net Configuration")
        if self.enabled and self.channel == "4Whats.net":
            if not settings.token or not settings.api_url or not settings.instance_id:
                frappe.throw(_("Please configure 4Whats.net settings to send WhatsApp messages"))
            
    def send(self, doc):
        context = get_context(doc)
        context = {"doc": doc, "alert": self, "comments": None}
        if doc.get("_comments"):
            context["comments"] = json.loads(doc.get("_comments"))

        if self.is_standard:
            self.load_standard_properties(context)
            
        try:
            if self.channel == '4Whats.net':
                self.send_whatsapp_msg(doc, context)
               
            elif self.channel == 'Maytapi':  # Changed from 'else self.channel == 'Maytapi':' to 'elif self.channel == 'Maytapi':'
                self.sendmsg(doc,context)
                
        except Exception as e:
            print(e)
            frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())
        super(ERPGulfNotification, self).send(doc)
            
        
    def sendmsg(self,doc,context):
        try:
            
            settings = frappe.get_doc("MAYTAPI CONFIGURATION")
            maytapi_key = settings.api_key
            message = frappe.render_template(self.message, context)
            start_index = message.find('^')
            end_index = message.rfind('^')
            # Extract the data between the delimiters
            site = message[start_index + 1:end_index]
            document = self.document_type
        
            try:
                recipients = self.getdata(document,site)
                
            except Exception as e:
                frappe.msgprint(str(e))
            
            try:
                for receipt in recipients:
                    message = frappe.render_template(self.message, context)   
                    phoneNumber = self.get_receiver_phone_number(receipt)
                    print(message,phoneNumber)
                    to_number = phoneNumber  # Replace with the recipient's phone number

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

                    response = requests.request("POST", settings.api_url, json=payload, headers=headers)
                    print(response)
            except Exception as e:
                frappe.msgprint(str(e))    
        
            
        except Exception as e:
            frappe.msgprint(str(e))
    
    def send_whatsapp_msg(self, doc, context):
        settings = frappe.get_doc("Four Whats Net Configuration")
        message = frappe.render_template(self.message, context)
        start_index = message.find('^')
        end_index = message.rfind('^')
        # Extract the data between the delimiters
        site = message[start_index + 1:end_index]
        document = self.document_type
       
        try:
            recipients = self.getdata(document,site)
     
        except Exception as e:
            frappe.msgprint(str(e))
        
        try:
            for receipt in recipients:
                message = frappe.render_template(self.message, context)   
                phoneNumber = self.get_receiver_phone_number(receipt)
                
                form_data = {
                    'id': phoneNumber,
                    'message': message
                }

                response = requests.post(settings.api_url, data=form_data)
               
        except Exception as e:
            frappe.msgprint(e)        
    
    def getdata(self,filter_document,filter_site):
        # Define the doctype and filter criteria
        doctype = 'Whatsapp Recipient'
        filter_document = filter_document  # Specify the document value you want to filter for
        filter_active = '1'  # Specify the 'active' value to filter for
        filter_site = filter_site  # Specify the 'site' value to filter for
        recipients=[]
        # Get all documents of the specified doctype
        all_documents = frappe.get_all(doctype)
        
        # Define the fields to extract from the parent document
        parent_fields_to_extract = ['name1', 'whatsapp_no', 'active']
        
        # Define the fields to extract from each child table entry
        child_fields_to_extract = ['site', 'document']
        
        # Iterate through each parent document
        for document in all_documents:
            parent_doc = frappe.get_doc(doctype, document['name'])
        
            # Access child table data
            child_table_data = parent_doc.get('permission')  # Assuming child table field name is 'permission'
        
            # Check if any child table entry has the specified 'document', 'active', and 'site' values
            has_filtered_entries = any(
                entry.get('document') == filter_document and
                entry.get('site') == filter_site
                for entry in child_table_data
            )
        
            # Check if the 'active' field matches the specified value
            has_filtered_active = str(parent_doc.get('active')) == str(filter_active)
        
            # If all filters match, merge selected fields from parent and child entries and log the combined details
            if has_filtered_entries and has_filtered_active:
            
                parent_data = {key: parent_doc.get(key) for key in parent_fields_to_extract}
            
        
                # Merge selected fields from parent with each child table entry
                for entry in child_table_data:
                    if (
                        entry.get('document') == filter_document and
                        entry.get('site') == filter_site
                    ):
                        child_data = {key: entry.get(key) for key in child_fields_to_extract}
                        merged_data = {**parent_data, **child_data}
                        
                        recipients.append(merged_data.get('whatsapp_no'))
        
        return recipients

    def get_receiver_phone_number(self, number):
        phoneNumber = number.replace("+", "").replace("-", "")
        if phoneNumber.startswith("+") == True:
            phoneNumber = phoneNumber[1:]
        elif phoneNumber.startswith("00") == True:
            phoneNumber = phoneNumber[2:]
        elif phoneNumber.startswith("0") == True:
            if len(phoneNumber) == 10:
                phoneNumber = "966" + phoneNumber[1:]
        else:
            if len(phoneNumber) < 10: 
                phoneNumber ="966" + phoneNumber
        if phoneNumber.startswith("0") == True:
            phoneNumber = phoneNumber[1:]
        
        return phoneNumber
