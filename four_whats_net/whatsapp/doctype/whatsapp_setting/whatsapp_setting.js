frappe.ui.form.on('Whatsapp Setting', {
    refresh: function(frm) {
        frm.add_custom_button('Initialize', function() {
            var url = frm.doc.init_url;
            var key = frm.doc.key;
            var token = frm.doc.token;

            console.log(url, key, token);

            frappe.call({
                method: 'four_whats_net.whatsapp.doctype.whatsapp_setting.whatsapp_api.initialise',
                args: {
                    url: url,
                    key: key,
                    token: token
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

        frm.add_custom_button('Get QR Code', function() {
            var qr_url = frm.doc.qr_url;
            var key = frm.doc.key;

            console.log(qr_url, key);

            frappe.call({
                method: 'four_whats_net.whatsapp.doctype.whatsapp_setting.whatsapp_api.get_qrcode',
                args: {
                    url: qr_url,
                    key: key
                },
                callback: function(response) {
                    console.log("Success: ", response);
                    if (response.message) {
                        // Attach the image to the attach_image field
                        frm.set_value('attach_image',"/files/" +response.message);
                        frappe.msgprint('Image attached successfully.');
                    } else {
                        frappe.msgprint('Error attaching image.');
                    }
                },
                error: function(err) {
                    console.log("Error: ", err);
                    frappe.msgprint('Error attaching image.');
                }
            });
        });
        // frm.add_custom_button('Get Status', function() {
        //     var qr_url = frm.doc.get_status;
        //     var key = frm.doc.key;

        //     console.log(qr_url, key);

        //     frappe.call({
        //         method: 'rsa_app.whatsapp.doctype.whatsapp_setting.whatsapp_api.get_status',
        //         args: {
        //             url: qr_url,
        //             key: key
        //         },
        //         callback: function(response) {
        //             console.log("Success: ", response);
        //             if (response.message) {
        //                 // Attach the image to the attach_image field
        //                 // frm.set_value('attach_image',"/files/" +response.message);
        //                 frappe.msgprint(response);
        //             } else {
        //                 frappe.msgprint('Error attaching image.');
        //             }
        //         },
        //         error: function(err) {
        //             console.log("Error: ", err);
        //             frappe.msgprint('Error attaching image.');
        //         }
        //     });
        // });
frm.add_custom_button('Get Status', function() {
    var qr_url = frm.doc.get_status;
    var key = frm.doc.key;

    console.log(qr_url, key);

    frappe.call({
        method: 'four_whats_net.whatsapp.doctype.whatsapp_setting.whatsapp_api.get_status',
        args: {
            url: qr_url,
            key: key
        },
        callback: function(response) {
            console.log("Success: ", response);
            if (response.message) {
                try {
                    var responseData = JSON.parse(response.message);

                    if (!responseData.error) {
                        var instanceData = responseData.instance_data;

                        var instanceKey = instanceData.instance_key;
                        var phoneConnected = instanceData.phone_connected;
                        var webhookUrl = instanceData.webhookUrl;
                        var userId = instanceData.user.id;
                        
                        console.log("Instance Key: ", instanceKey);
                        console.log("Phone Connected: ", phoneConnected);
                        frm.set_value('phone_connected',phoneConnected);
                        console.log("Webhook URL: ", webhookUrl);
                        console.log("User ID: ", userId);
                        frm.set_value('user_id',userId);
                        var statusText = (phoneConnected) ? 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXID-OKQIXTiCZ5lsIKvrYyb0XDBRJRr4SyAv_MCbMA_moVYRP3ahMWJR5FzIxS4skFds&usqp=CAU' : 'https://aabelmedia.files.wordpress.com/2015/12/whatsapp-ban-481967.jpg';
                        frm.set_value('attach_image',statusText);
                        // Perform actions with the extracted fields as needed
                    } else {
                        frappe.msgprint('Error fetching instance data.');
                    }
                } catch (error) {
                    console.log("Error parsing message: ", error);
                    frappe.msgprint('Error parsing message.');
                }
            } else {
                frappe.msgprint('No message received.');
            }
        },
        error: function(err) {
            console.log("Error: ", err);
            frappe.msgprint('Error fetching instance data.');
        }
    });
});


    }
});

