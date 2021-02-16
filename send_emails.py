#!/usr/bin/env python3

import smtplib,os
from email.message import EmailMessage
import dotenv
from dotenv import load_dotenv

load_dotenv()

class email_client:

    #load variables set in your .env file
    def __init__(self,new_sender_name,new_sender_email,new_sender_password):
        #Initilizes bot with class-wide variables
        self.sender_name=new_sender_name
        self.sender_email=new_sender_email
        self.email_password=new_sender_password

    def send_email(self,message):
        print("Sending email...\n")

        msg= EmailMessage()
        msg.set_content(message)
        msg['subject'] = "PS5"
        msg['to']= str(os.getenv('RECIPIENT_EMAIL'))
        msg['from'] = str(os.getenv('SENDER_EMAIL'))

        #setup email server, email host , and common used port 
        server = smtplib.SMTP('smtp.gmail.com',587)
        
        #encrypts smtp commands
        server.starttls()

        #Login to senders' email account 
        server.login(self.sender_email, self.email_password)

        #Send the email
        server.send_message(msg)
        server.quit()
        pass
        print("Email Sent. \n")

"""if __name__ == '__main__':

    new_user = email_client("John",str(os.getenv('SENDER_EMAIL')),str(os.getenv('EMAIL_PASSWORD')))
    new_user.send_email()"""
