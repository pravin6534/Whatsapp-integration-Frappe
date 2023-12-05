// Copyright (c) 2023, hts-qatar and contributors
// For license information, please see license.txt

frappe.ui.form.on('MAYTAPI CONFIGURATION', {
    refresh: function(frm) {
        frm.add_custom_button('TEST MSG', function() {
            var url = frm.doc.api_url;
            var key = frm.doc.api_key;
            var whatsapp_number = frm.doc.whatsapp_number;
			var test_message = frm.doc.test_message;

            console.log(url, key, whatsapp_number,test_message);

            frappe.call({
                method: 'four_whats_net.four_whats_net.doctype.maytapi_configuration.maytapitest.sendmsg',
                args: {
                    url: url,
                    key: key,
                    contact: whatsapp_number,
					message: test_message
                },
                callback: function(response) {
                    console.log("Success: ", response);
                    // Handle success response as needed
                },
                error: function(err) {
                    console.log("Error: ", err);
                    // Handle error response as needed
                }
            });
        });
	}});