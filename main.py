import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import time
from email.header import Header
from email.utils import formataddr
#==================================================================
subject = input(" [+] Enter your Subject Line here-> ")
sender_name = input("[+] Enter here sender name->")
#==================================================================
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.ehlo()
#==================================================================
# HTML Message here..
with open('mail.html', 'r', encoding="utf8") as file:
    data = file.read().replace('\n', '')
count = 0
#==================================================================
# Open File and Reading Smtp server List
with open("smtp.csv") as file:
    reader = csv.reader(file)
    next(reader)
    #=================================================================
    for mail, password, in reader:
        server.login(mail, password)
        #=================================================================
        # Client Email List
        with open("mail_list.csv") as file:
            reader = csv.reader(file)
            next(reader)
            #==================================================================
            for email, in reader:
                #==================================================================
                message = MIMEMultipart("alternative")
                message["Subject"] = (subject)
                #=================================================================
                message["From"] = formataddr((str(Header(sender_name, 'utf-8')), email))
                #==================================================================
                # Html message that you have set
                html = data.format()
                #==================================================================
                message.attach(MIMEText(html, "html"))
                #==================================================================
                server.sendmail(mail, email, message.as_string())
                #==================================================================
                count += 1
                print(str(count) + ". Sent to " + email)

                if (count % 1000 == 0):
                    server.quit()
                    print("Server cooldown for 100 seconds")
                    time.sleep(100)
                    server.ehlo()
                    server.login(mail, password)
                    # Finally Sever Quit
                    server.quit()
                #=================================================================
