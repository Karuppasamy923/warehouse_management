# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    data, columns = [], []
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    profit = get_profit(data)
    return columns, data, None, chart,profit

def get_columns():
    columns = [
        {"fieldname": field, "label": label, "fieldtype": fieldtype, "width": "100"}
        for field, label, fieldtype in [
            ("company_name", "Company Name", "Data"),
            ("type", "Type", "Data"),
            ("meditor_name", "Meditor Name", "Data"),
            ("product_id", "Product Id", "Data"),
            ("product_name", "Product Name", "Data"),
            ("product_quantity", "Product Quantity", "Int"),
            ("product_price", "Product Price", "Int"),
            ("total_amount", "Total Amount", "Int")
        ]
    ]
    return columns

def get_data(filters):
    data = frappe.get_all("Transaction", filters=filters, fields=["*"])
    return data

def get_chart_data(data):
    if not data:
        return None
    labels = ["Sold", "Purchased","Stock"]
    products = {
        "Sold": 0,
        "Purchased": 0,
        "Stock":0
    }
    datasets = []
    for details in data:
        if details.get("type") == "Sales":
            products["Sold"] += details.get("product_quantity")
        elif details.get("type") == "Purchase":
            products["Purchased"] += details.get("product_quantity") 
    datasets.append({
        "values": [products.get("Sold"), products.get("Purchased"),products.get("Purchased")-products.get("Sold")]
    })
    chart = {
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "type": "bar",
        "height": "300"
    }
    return chart

def get_profit(data):
    sell=0
    buy=0
    for details in data:
        rate,mrp=frappe.db.get_value("Product",details.get("product_id"),["sales_rate","mrp_rate"])
        sell += int(mrp)*int(details.get("product_quantity"))
        buy += int(rate)*int(details.get("product_quantity"))
    sprofit=(sell-buy)/buy
    profit=sprofit*100    
    profit=format(profit, '.2f')
    return [
    {
        "value":str(profit)+"%",
        "indicator":"Green",
        "label":"Profit",
        "fieldtype":"Data"
    },
    {
        "value":"0%",
        "indicator":"Red",
        "label":"Loss",
        "fieldtype":"Data"
    }

    ]   