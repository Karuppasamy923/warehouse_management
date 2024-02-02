frappe.query_reports["Transaction report"] = {
    "filters": [
        {
            "fieldname": "company_name",
            "label": "Company Name",
            "fieldtype": "Link",
            "options": "Company"
        },
        {
            "fieldname": "product_type",
            "label": "Product Type",
            "fieldtype": "Data",
            //"options": "\nSales\nPurchase"
        },
        {
            "fieldname": "product_id",
            "label": "Product Id",
            "fieldtype": "Link",
            "options": "Product"
        },
        {
            "fieldname": "product_quantity",
            "label": "Product Quantity",
            "fieldtype": "Int"
        }
    ]
}    