import imaplib
import smtplib
import email
import uuid
from datetime import datetime
import pytz
from data import insertDataIntoUserEmailTable, insertDataIntoUserComplainTable
import re


def extract_Imp_Info(email_body):

    identifiedIssue = ""
    identifiedAmount = ""
    identifiedID = ""
    identifiedContact = ""
    identifiedTime = ""

    amount_pattern = re.compile(r'(?:PKR|Rs)\s*\d{1,}(?:\.\d{2})?')
    contact_number_pattern = re.compile(r'(?:(?:\+?\d{2}\s*)?(?:\d{4}|\(\d{4}\))[\s-]?\d{3}[\s-]?\d{4})')
    transaction_id_pattern = re.compile(r'ID#[0-9]+', re.IGNORECASE)
    transaction_time_pattern = re.compile(r'\b\d{1,2}:\d{2} ?(?:AM|PM|am|pm)\b')
    

    # Find matches in the email body
    amount_matches = amount_pattern.findall(email_body)
    contact_matches = contact_number_pattern.findall(email_body)
    transaction_id_matches = transaction_id_pattern.findall(email_body)
    transaction_time_matches = transaction_time_pattern.findall(email_body)

    # Extract information from matches
    amounts = amount_matches
    contact = contact_matches
    transaction_ids = transaction_id_matches
    transaction_times = transaction_time_matches

    # Print extracted amounts
    print(f"Extracted Amounts: {amounts}")
    print(f"Extracted Contact: {contact}")
    print(f"Extracted Transaction ID: {transaction_ids}")
    print(f"Extracted Transaction Time: {transaction_times}")

    if(len(amounts) > 0 or len(transaction_ids) > 0):
        identifiedIssue = "Money Transfer"

        if(len(amounts) > 0):
            identifiedAmount = str(amounts[0])
        else:
            identifiedAmount = "Unidentified"

        if(len(contact) > 0):
            identifiedContact = str(contact[0])
        else:
            identifiedContact = "Unidentified"

        if(len(transaction_ids) > 0):
            identifiedID = str(transaction_ids[0])
        else:
            identifiedID = "Unidentified"

        if(len(transaction_times) > 0):
            identifiedTime = str(transaction_times[0])
        else:
            identifiedTime = "Unidentified"
    
    return identifiedIssue, identifiedAmount, identifiedContact, identifiedID, identifiedTime


def extract_first_email_address(email_string):
    # Split the text by space
    words = email_string.split()
    
    # Check if there are any words
    if words:
        # Return the first word
        return words[0]
    else:
        # If no words are found, return None
        return None

# Email account credentials
EMAIL = 'easypaisa@blinkitech.com'
PASSWORD = 'Telenor@123'

# IMAP server settings for Outlook
IMAP_SERVER = 'mail.blinkitech.com'
IMAP_PORT = 993

# SMTP server settings for Outlook
SMTP_SERVER = 'mail.blinkitech.com'
SMTP_PORT = 465

def check_email():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Search for unseen emails
    result, data = mail.search(None, 'UNSEEN')

    if result == 'OK':
        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                sender_email = msg['From']
                
                if msg.is_multipart():
                    # If the email message is multipart, iterate over its parts
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == 'text/plain' or content_type == 'text/html':
                            # Get the payload (body) of the email part
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    # If the email message is not multipart, simply get its payload (body)
                    body = msg.get_payload(decode=True).decode()

                guid = str(uuid.uuid4())

                pkt_timezone = pytz.timezone('Asia/Karachi')
                current_datetime_pkt = datetime.now(pkt_timezone)

                guid = str(guid)
                sender_email = str(sender_email)
                first_email = extract_first_email_address(sender_email)
                sender_email = first_email
                body = str(body)
                current_datetime_pkt = str(current_datetime_pkt)


                print("*******************************************")
                print(f"GUID: {guid}")
                print(f"EMAIL: {sender_email}")
                print(f"EMAIL BODY: {body}")
                print(f"DATE TIME: {current_datetime_pkt}")
                print("*******************************************")

                identifiedIssue, identifiedAmount, identifiedContact, identifiedID, identifiedTime = extract_Imp_Info(body)

                insertDataIntoUserEmailTable(guid,sender_email, body, current_datetime_pkt)
                insertDataIntoUserComplainTable(guid, body, "Acknowledgement Email", identifiedContact, identifiedIssue,
                                                 identifiedAmount, identifiedID, identifiedTime, "Your Comment Here")
                

                print(f"Replying to: {sender_email}")
                reply_to_sender(sender_email, msg, guid)
                print("DONE")

    # Close the connection
    mail.close()
    mail.logout()

def reply_to_sender(sender, msg, guid):
    
    # Connect to the SMTP server
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(EMAIL, PASSWORD)

    # Compose the reply email
    subject = "Acknowledgement of Your Query: We're Here to Help!"
    body = 'Dear Customer,\nI hope this email finds you well.\n\nI wanted to take a moment to acknowledge the query you recently submitted to us. Your feedback and inquiries are invaluable to us as they help us continually improve our services to better meet your needs.\n\nAdditionally, if you ever encounter any issues or have feedback about our services, we encourage you to use our dedicated complaints portal, where you can share your concerns transparently. You can access the portal through the following link:\nhttps://easypaisaresponse.azurewebsites.net/email?guid={}\n\nThank You for your patience and understanding.\n\nBest Regards\nYour Company Support Team'.format(guid)
    message = f'Subject: {subject}\n\n{body}'

    # Send the reply email
    server.sendmail(EMAIL, sender, message)

    # Close the connection
    server.quit()
    print("Reply sent successfully.")

    #except smtplib.SMTPRecipientsRefused as e:
    #    print(f"Failed to send reply to {sender}: {e}")
    #except Exception as e:
    #    print(f"An error occurred while sending reply to {sender}: {e}")