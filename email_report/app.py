import boto3
from datetime import datetime, timedelta
import pytz

def lambda_handler(event, context):
    days_back = 1
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ChatbotTable')
    now = datetime.now(pytz.timezone('US/Pacific'))
    twenty_four_hours_ago = now - timedelta(hours=days_back * 24)
    twenty_four_hours_ago_timestamp = int(twenty_four_hours_ago.timestamp())

    # Scan the DynamoDB table for relevant entries
    response = table.scan(
        FilterExpression='#ts >= :timestamp',
        ExpressionAttributeNames={
            '#ts': 'timestamp',
        },
        ExpressionAttributeValues={
            ':timestamp': twenty_four_hours_ago_timestamp
        }
    )

    # Convert Decimal to int for comparison, and sort the list of dictionaries
    sorted_items = sorted(response['Items'], key=lambda x:  x['timestamp'])

    # Update the original dictionary with the sorted list
    response['Items'] = sorted_items

    email_body = ''
    for item in response['Items']:
        utc_dt = datetime.utcfromtimestamp(int(item['timestamp'])).replace(tzinfo=pytz.utc)
        pacific_dt = utc_dt.astimezone(pytz.timezone('US/Pacific'))
        formatted_time = pacific_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

        email_body += f"User UUID: {item['user_uuid']}\n"
        email_body += f"IP Address: {item['ip_address']}\n"
        email_body += f"Timestamp: {formatted_time}\n"
        email_body += f"Input: {item['input']}\n"
        email_body += f"Output: {item['output']}\n\n"

    if not email_body:
        email_body += f"No interactions in the past {days_back} days"

    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='FROM_EMAIL', WithDecryption=True)
    from_email = parameter['Parameter']['Value']


    # Send the email using AWS SES
    ses = boto3.client('ses')
    ses.send_email(
        Source=from_email,
        Destination={
            'ToAddresses': [from_email]
        },
        Message={
            'Subject': {
                'Data': f"Daily Report for {now.strftime('%m-%d-%Y')}"
            },
            'Body': {
                'Text': {
                    'Data': email_body
                }
            }
        }
    )


if __name__ == '__main__':
    lambda_handler({}, {})
