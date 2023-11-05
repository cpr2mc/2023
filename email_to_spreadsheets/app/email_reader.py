from googleapiclient.discovery import build
from auth import create_credentials

def get_gmail_service():
    credentials = create_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    return service

def list_messages_with_subject(service, user_id='me', subject_query='para_lead'):
    """
    List all messages of the user's mailbox with a subject containing the given query.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
                 can be used to indicate the authenticated user.
        subject_query: String to search in the subject line of the emails.

    Returns:
        List of messages that meet the criteria of the query. 
        Note that the returned list contains message IDs and thread IDs.
    """
    try:
        query = f'subject:{subject_query}'
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get('messages', [])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response.get('messages', []))

        return messages
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def get_message(service, user_id, message_id):
    # Call the Gmail API to fetch a specific message
    pass

def parse_message(message):
    # Extract the relevant information from the message
    pass

# Example of calling the list_messages_with_subject function:
if __name__ == '__main__':
    service = get_gmail_service()
    messages = list_messages_with_subject(service, subject_query='para_lead')
    print(f"Total messages with 'para_lead' in subject: {len(messages)}")
    for message in messages:
        print(f"Message ID: {message['id']}")
