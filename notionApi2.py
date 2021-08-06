# Check how to create integration (https://developers.notion.com/docs/getting-started)
#export NOTION_TOKEN=<<YOUR-TOKEN>>
#export SENDGRID_API_KEY=<<YOUR-TOKEN>>
#pip install notion-client
#setup https://app.sendgrid.com/settings/sender_auth/senders

import os
import random
from notion_client import Client
from pprint import pprint
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

DATABASE_ID="2bcd4d6ee067419ca29ce96c535b0357"
SENDER_EMAIL="midoss17@gmail.com"
RECEIVER_EMAIL="midoss17@gmail.com"
QUOTE_COL_NAME="Quote"
BOOK_COL_NAME="Book"
AUTHOR_COL_NAME="Author"
NumberOfQuotes = 3

def send_email_using_sendgrid(message_content):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(SENDER_EMAIL)  
    to_email = To(RECEIVER_EMAIL)
    subject = "Three Quotes of the Day"
    content = Content("text/plain", message_content)
    mail = Mail(from_email, to_email, subject, content)
    #mail.template_id = "d-3218314e84194ce386e87d2c52e5a4bd"

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    if(response.status_code == 202):
        print("Message sent successfully")
    #print(response.status_code)
    #print(response.headers)

def transform_quotes_list_to_html_message_content(quotes):
    html_output = ""
    for quote_item in quotes:
        html_output += quote_item[0] + "\n"
        html_output += quote_item[1] + "\n"
        html_output += quote_item[2] +"\n"
        html_output += "\n\n"
    return html_output

# Col_type can be ["rich_text", "title"]
def get_data_from_DB(my_page, db_row_idx, col_name, col_type):
    
    return my_page["results"][db_row_idx]["properties"][col_name][col_type][0]["plain_text"]

def update_data_inside_DB(my_page, db_row_idx, col_name, col_type, new_value):
    
    my_page["results"][db_row_idx]["properties"][col_name][col_type][0]["plain_text"] = new_value

token_v2 = os.environ['NOTION_TOKEN']
if not token_v2:
    raise Exception('Please set a token in the code or your environment.')
notion = Client(auth=os.environ["NOTION_TOKEN"])

list_users_response = notion.users.list()
#pprint(list_users_response)

my_page = notion.databases.query(
    **{
        "database_id": DATABASE_ID,
    }
)
num_db_entries = len(my_page["results"])

#print(num_db_entries)

quotes = []
for i in range(NumberOfQuotes):
    rand_idx = random.randint(0, num_db_entries-1)
    quote_name = get_data_from_DB(my_page, rand_idx, QUOTE_COL_NAME, "title")
    book_name = get_data_from_DB(my_page, rand_idx, BOOK_COL_NAME, "rich_text")
    author_name = get_data_from_DB(my_page, rand_idx, AUTHOR_COL_NAME, "rich_text")
    quotes.append((quote_name, book_name, author_name))
    print(quote_name, book_name, author_name)
    
html_message_content = transform_quotes_list_to_html_message_content(quotes)
send_email_using_sendgrid(html_message_content)

