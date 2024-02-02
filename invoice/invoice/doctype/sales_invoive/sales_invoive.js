// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt
var customer="";
var company="";
frappe.ui.form.on('Product_details',{
	product:function(frm,cdt,cdn){
		get_rate(frm,cdt,cdn)
	},
	quantity:function(frm,cdt,cdn){
		calculate(frm,cdt,cdn)
	}
});
frappe.ui.form.on('Sales_invoive',{
	customer_name:function(frm){
		var cus=frm.doc.customer_name;
		if(cus){
			customer=cus;
			//frappe.msgprint(customer);
		}
	},
	company_name:function(frm){
		var com=frm.doc.company_name;
		if(com){
			company=com;
			//frappe.msgprint(company);
		}
	}
})
frappe.ui.form.on('Sales_invoive', {
	on_submit:function(frm){
		put_data(frm);
	}
});
function put_data(frm){
	frappe.call({
		method:"invoice.invoice.doctype.sales_invoive.sales_invoive.get_data",
		args:{
			'_company':company,
			'_customer':customer
		},
		callback:function(res){
			frappe.msgprint(res.message)
		}
	})
}
function get_rate(frm,cdt,cdn){
	var child=locals[cdt][cdn];
	var product=child.product;
	frappe.call({
		method:"invoice.invoice.doctype.sales_invoive.sales_invoive.get_price",
		args:{
			'id':product
		},
		callback:function(res){
			//frappe.msgprint(res.message)
			var price = parseInt(res.message);
            frappe.model.set_value(cdt, cdn, 'price', price);
		}
	})
}
function calculate(frm,cdt,cdn){
	var child=locals[cdt][cdn];
	var tot=child.quantity*child.price;
	frappe.model.set_value(cdt, cdn, 'total', tot);
}