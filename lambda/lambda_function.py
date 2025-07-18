import json
import boto3
import datetime

def lambda_handler(event, context):
    print("Event received:", event)

    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:ap-northeast-2:your_account_id:YourTopicName',
        Message=f"Docker image pushed at {datetime.datetime.now()}",
        Subject="Docker Deployment Notification"
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }
