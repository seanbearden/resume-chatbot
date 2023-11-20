import boto3
from datetime import datetime, timedelta
import os
import pytz


def lambda_handler(event, context):
    days_back = 1
    last_updated = 'LastUpdated'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['SESSION_TABLE_NAME'])
    now = datetime.now(pytz.timezone('US/Pacific'))

    # Calculate the timestamp for 24 hours ago
    twenty_four_hours_ago = datetime.now() - timedelta(days=days_back)
    twenty_four_hours_ago_timestamp = twenty_four_hours_ago.isoformat()

    # Scan the DynamoDB table for relevant entries
    response = table.scan(
        FilterExpression='#ts >= :timestamp',
        ExpressionAttributeNames={
            '#ts': last_updated,  # Replace with the actual name of your timestamp attribute
        },
        ExpressionAttributeValues={
            ':timestamp': twenty_four_hours_ago_timestamp
        }
    )

    # Convert Decimal to int for comparison, and sort the list of dictionaries
    sorted_items = sorted(response['Items'], key=lambda x:  x[last_updated])

    # Update the original dictionary with the sorted list
    response['Items'] = sorted_items

    email_body = ''
    for item in response['Items']:
        formatted_time = item[last_updated]

        email_body += f"User UUID: {item['SessionId']}\n"
        email_body += f"Timestamp: {formatted_time}\n\n"
        for message in item.get('History', []):
            content = message.get('data', {}).get('content', '')
            if message['type'] == 'human':
                email_body += f"Human: {content}\n\n"
            elif message['type'] == 'ai':
                email_body += f"AI: {content}\n\n"
            else:
                email_body += f"UNKNOWN: {content}\n\n"

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
