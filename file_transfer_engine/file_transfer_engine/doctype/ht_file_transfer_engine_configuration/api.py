import frappe
import datetime
from frappe.utils import now

from crontab import CronTab
import os

from frappe.model.document import Document

def initiateJob(cronExp, sourceFTM, sourceHostAddress, sourcePort, sourceUsername, sourcePassword, sourceFolder, destinationFTM, destinationHostAddress, destinationAPIURL, destinationPort, destinationUsername, destinationPassword, destinationFolder, docID, destinationAPIToken):

    job_command = cronExp +' python3 '+ os.getcwd() +'/../apps/file_transfer_engine/file_transfer_engine/file_transfer_engine/doctype/ht_file_transfer_engine_configuration/file_transfer_engine.py '+ docID +' >> '+ os.path.expanduser( '~' ) +'/cronJob.log 2>&1'
    job_command = ' python3 '+ os.getcwd() +'/../apps/file_transfer_engine/file_transfer_engine/file_transfer_engine/doctype/ht_file_transfer_engine_configuration/file_transfer_engine.py '+ docID +' >> '+ os.path.expanduser( '~' ) +'/cronJob.log 2>&1'

    #with open('/var/spool/cron/crontabs/frappe-alex', 'a') as f:
    #    f.write('\n'+ job_command +'\n')
    #    print('Cron job added successfully!')
    # define the command to be run
    command = "/path/to/your/command"

    # define the cron schedule using the standard crontab syntax
    # here, the command will run every day at 5 AM
    cron_schedule = "0 5 * * *"

    # add the cron job to the current user's crontab
    os.system(f'(crontab -l ; echo "{cronExp} {job_command}") | sort - | uniq - | crontab -')

#Currently not in use
@frappe.whitelist()
def updateJob(engineID):
    doc = frappe.get_doc('HT File Transfer Engine configuration', engineID)
    print(doc)
    frappe.response['message'] = doc
    # To insert in HT File Transfer Engine configuration' doctype

@frappe.whitelist()
def fetchJobConfig(engineID):
    doc = frappe.get_doc('HT File Transfer Engine configuration', engineID)
    print(doc)
    frappe.response['message'] = doc
    # To insert in HT File Transfer Engine configuration' doctype

@frappe.whitelist()
def deletedoc(**inputValues):
    doc = frappe.get_doc('HT File Transfer Engine configuration',inputValues.get('name'))
    doc.delete()
    frappe.db.commit()
    print("delete doc")
    frappe.msgprint('Deleted')
    #frappe.delete_doc('HT File Transfer Engine configuration',name)

@frappe.whitelist()
def addFileTransferEngineConfig(**inputValues):
    engineDoc = frappe.get_doc({'doctype': 'HT File Transfer Engine configuration', 'source_file_transfer_type': inputValues.get('sourceFTM'), 'source_hostname_or_ip_address': inputValues.get('sourceHostAddress'), 'source_port': inputValues.get('sourcePort'), 'source_username': inputValues.get('sourceUsername'), 'source_password': inputValues.get('sourcePassword'), 'source_folder': inputValues.get('sourceFolder'), 'destination_file_transfer_type': inputValues.get('destinationFTM'), 'destination_hostname_or_ip_address': inputValues.get('destinationHostAddress'), 'destination_api_url':  inputValues.get('destinationAPIURL'), 'destination_port':  inputValues.get('destinationPort'), 'destination_username':  inputValues.get('destinationUsername'), 'destination_password':  inputValues.get('destinationPassword'), 'destination_folder': inputValues.get('destinationFolder'), 'destination_api_token': inputValues.get('destinationAPIToken') , 'configuration_name': inputValues.get('configurationName'), 'scheduler_cron_expression': inputValues.get('cronExpression') })
    engineDoc.insert(ignore_permissions=True)

    engineDoc.submit()
    docID = engineDoc.name
    frappe.db.commit()

    initiateJob(inputValues.get('cronExpression', '*/10 * * * *'), inputValues.get('sourceFTM'), inputValues.get('sourceHostAddress'), inputValues.get('sourcePort'), inputValues.get('sourceUsername'), inputValues.get('sourcePassword'), inputValues.get('sourceFolder'), inputValues.get('destinationFTM'), inputValues.get('destinationHostAddress'), inputValues.get('destinationAPIURL'), inputValues.get('destinationPort'), inputValues.get('destinationUsername'), inputValues.get('destinationPassword'), inputValues.get('destinationFolder'), docID, inputValues.get('destinationAPIToken'))

@frappe.whitelist()
def getSchedulerList():
    doc = frappe.get_list('HT File Transfer Engine configuration', fields=['configuration_name', 'alert_enable', 'source_recipients_mail_list', 'destination_recipients_mail_list', 'source_file_transfer_type', 'source_hostname_or_ip_address', 'source_username', 'source_password', 'source_port', 'source_folder', 'destination_file_transfer_type', 'destination_api_url', 'destination_port', 'destination_username', 'destination_password', 'destination_api_token', 'destination_folder', 'scheduler_cron_expression', 'destination_hostname_or_ip_address'])
    print(len(doc))
    frappe.response['message'] = doc

