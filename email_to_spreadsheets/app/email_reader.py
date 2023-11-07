# this is all built in conjuction with chatGPT
import base64

from googleapiclient.discovery import build
from auth import create_credentials

def get_gmail_service():
    credentials = create_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    return service

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def list_messages_matching_query(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def display_emails_containing_para_lead():
    # Get credentials and create a service
    credentials = create_credentials()
    service = build('gmail', 'v1', credentials=credentials)

    # List all messages with 'para_lead' in the subject
    messages = list_messages_matching_query(service, 'me', query='subject:para_lead')

    if not messages:
        print('No messages found.')
    else:
        print(f'Found {len(messages)} messages:')
        for message in messages:
            msg = get_message(service, 'me', message['id'])

            # Get subject from the message
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
            print(f'Subject: {subject}')

            # Get and decode the email body from the message payload
            parts = msg['payload'].get('parts', [])
            for part in parts:
                # Check if the part contains 'text/plain' or 'text/html'
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    body_data = part['body']['data']
                    body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                    print(f'Body: {body}\n')
                elif part.get('parts'):  # Nested parts, could be a multipart/alternative
                    # Go through each part in the nested parts
                    for subpart in part['parts']:
                        if subpart['mimeType'] == 'text/plain' or subpart['mimeType'] == 'text/html':
                            body_data = subpart['body']['data']
                            body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                            print(f'Body: {body}\n')

# Example of calling the display_emails_containing_para_lead function:
if __name__ == '__main__':
    display_emails_containing_para_lead()


# Call the function to display the emails
display_emails_containing_para_lead()

def parse_message(message):
    # Extract the relevant information from the message
    pass

