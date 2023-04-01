import frappe
import datetime
from frappe.utils import now

@frappe.whitelist()
def getTransferAudit():
    print('AAAAAAAABBBBB')
    doc = frappe.get_list('HT File Transfer Results', fields=['file_name','source_folder','destination_folder','transfer_status','transferred_date_time', 'transferred_failure_reason', 'transferred_file_size'])
    print('Fetch Data')
    frappe.response['message'] = doc
    #frappe.delete_doc('HT File Transfer Engine configuration',name)


@frappe.whitelist()
def updateReport(**inputValues):
    reportDoc = frappe.get_doc({'doctype': 'HT File Transfer Results', 'file_name': inputValues.get('filename'), 'transfer_status': inputValues.get('status'), 'transferred_date_time': now(), 'transferred_file_size': inputValues.get('fileSize'), 'transferred_failure_reason': inputValues.get('failureReason'), 'source_folder':  inputValues.get('sourceFolder'), 'destination_folder': inputValues.get('destinationFolder') })
    reportDoc.insert(ignore_permissions=True)
    reportDoc.submit()
    frappe.db.commit()

