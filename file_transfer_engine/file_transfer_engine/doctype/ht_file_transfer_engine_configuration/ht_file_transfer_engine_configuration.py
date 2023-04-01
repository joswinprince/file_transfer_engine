# Copyright (c) 2023, Hephzibah Technolofies Inc and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class HTFileTransferEngineconfiguration(Document):
    def method(self):
        frappe.msgprint("doctype py called")
