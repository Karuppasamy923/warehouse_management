# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Sales_invoive(Document):
    def on_submit(self):
        global docN,doc
        doc=self
        docN=self.name

@frappe.whitelist()
def get_price(id):
    value=frappe.db.get_value("Product",{'product_id':id},'mrp_rate')
    return str(value)

@frappe.whitelist()
def get_data(_company,_customer):
    # frappe.msgprint(_customer)
    #sales=frappe.get_doc('Sales_invoive',docN)
    for row in doc.sales_details:
        child=frappe.get_doc('Product',row.product)
        cqty,cp=frappe.db.get_value('Product',row.product,['sold_quantity','sold_price'])
        frappe.db.set_value('Product',row.product,'sold_quantity',int(row.quantity)+int(cqty))
        frappe.db.set_value('Product',row.product,'sold_price',int(row.total)+int(cp))
        new=frappe.new_doc('Transaction')
        new.company_name=_company
        new.type="Sales"
        new.mediator_type="Customer"
        new.meditor_name=_customer
        new.product_id=row.product
        new.product_name=child.product_name
        new.product_quantity=row.quantity
        new.product_price=row.price
        new.total_amount=row.total
        new.insert()
    
