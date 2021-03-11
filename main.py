#!/usr/bin/env python3


from nikebot import *
from dotenv import load_dotenv



amt=2
counter=0
while counter<amt:
    load_dotenv()
    notification= email_client("Alex",str(os.getenv('SENDER_EMAIL')),str(os.getenv('EMAIL_PASSWORD')))
    new_user = nike_bot(str(os.getenv('NIKE_EMAIL')),str(os.getenv('NIKE_PASSWORD')))
    try:
        if new_user.findProduct() == 1:
            notification.send_email("Nike shoe order placed, check your email")
            counter +=1
    except:
        pass
    time.sleep(random.randint(30,50))