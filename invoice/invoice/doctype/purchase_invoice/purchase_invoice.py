import frappe
from frappe.model.document import Document

class Purchase_invoice(Document):
    def on_submit(self):
        for row in self.purchase_details:
            child = frappe.get_doc('Product', row.product)
            cqty,cp=frappe.db.get_value('Product',row.product,['purchase_quantity','purchased_price'])
            frappe.db.set_value('Product',row.product,'purchase_quantity',int(row.quantity)+int(cqty))
            frappe.db.set_value('Product',row.product,'purchased_price',int(row.total)+int(cp))
            new_transaction = frappe.new_doc('Transaction')
            new_transaction.company_name = self.company_name
            new_transaction.type = "Purchase"
            new_transaction.mediator_type = "Supplier"
            new_transaction.meditor_name = self.supplier_name
            new_transaction.product_id = row.product
            new_transaction.product_name = child.product_name
            new_transaction.product_quantity = row.quantity
            new_transaction.product_price = row.price
            new_transaction.total_amount = row.total
            new_transaction.insert()

@frappe.whitelist()
def get_price(id):
    value = frappe.db.get_value("Product", {'product_id': id}, 'sales_rate')
    return str(value)

@frappe.whitelist()
def get_data(_company, _supplier):
    pass
