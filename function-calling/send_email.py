#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   send_email.py
@Time    :   2023/06/17 11:51:24
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   Send Emails with OpenAI Function Calling
"""

import os
import openai
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

openai.api_key = os.getenv("OPENAI_KEY")
# email server address and port
smtp_server = 'smtp.163.com'
smtp_port = 465

# sender email address and password
sender_email = os.environ.get('EMAIL_ADDRESS')
password = os.environ.get('EMAIL_PASSWORD')


def send_email(receiver_email, subject, body):
    """send the user an email with the answer"""

    try:

        # Create a multipart message and set headers
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # create SMTP session
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)  # sender email password

            # send the email
            server.send_message(msg)
        return json.dumps({"body": "Email sent successfully"})

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def run_conversation(content):
    """run the conversation with the user and send the email

    Args:
        content (_type_): user input
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{
            "role": "user",
            "content": content
        }],
        functions=[{
            "name": "send_email",
            "description": "Sends an email to the specified email address",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "An email address to send the email to",
                    },
                    "body": {
                        "type": "string"
                    },
                    "subject": {
                        "type": "string"
                    },
                },
            },
        }],
        function_call="auto",
    )

    message = response["choices"][0]["message"]
    print('message: ', message)

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        print('function_name: ', function_name)

        # Access the arguments
        arguments = json.loads(message['function_call']['arguments'])
        email_arg = arguments['email']
        body_arg = arguments['body']
        subject_arg = arguments['subject']

        # Step 3, call the function
        function_response = send_email(email_arg, subject_arg, body_arg)

        print(function_response)


# test send email
# send_email('huyidada@gmail.com', 'test', 'This is a test email, please ignore it')

content = "send an email to huyidada@gmail.com about how to use OpenAI API to implement chat Q&A services"
print(run_conversation(content))