frappe.ui.form.on('Product_details', {
    product: function (frm, cdt, cdn) {
        get_rate(frm, cdt, cdn);
    },
    quantity: function (frm, cdt, cdn) {
        calculate(frm, cdt, cdn);
    }
});

frappe.ui.form.on('Purchase_invoice', {
    supplier_name: function (frm) {
        var sub = frm.doc.supplier_name;
        if (sub) {
            supplier = sub;
        }
    },
    company_name: function (frm) {
        var com = frm.doc.company_name;
        if (com) {
            company = com;
        }
    }
});

frappe.ui.form.on('Purchase_invoice', {
    on_submit: function (frm) {
        put_data(frm);
    }
});

function put_data(frm) {
    frappe.call({
        method: "invoice.invoice.doctype.purchase_invoice.purchase_invoice.get_data",
        args: {
            '_company': company,
            '_supplier': supplier
        },
        callback: function (res) {
            frappe.msgprint(res.message);
        }
    });
}

function get_rate(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    var product = child.product;
    frappe.call({
        method: "invoice.invoice.doctype.purchase_invoice.purchase_invoice.get_price",
        args: {
            'id': product
        },
        callback: function (res) {
            var price = parseInt(res.message);
            frappe.model.set_value(cdt, cdn, 'price', price);
        }
    });
}

function calculate(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    var tot = child.quantity * child.price;
    frappe.model.set_value(cdt, cdn, 'total', tot);
}
