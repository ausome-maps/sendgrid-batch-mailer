from sendgrid import SendGridAPIClient
import os
import base64
from sendgrid.helpers.mail import (
    Email, Mail, To, Attachment, FileContent, FileName,
    FileType, Disposition, Content, ContentId)
import csv
  
# Open file 
with open('file_name.csv',encoding='latin-1') as file_obj: # Change to file name of csv for batch mailing
      
    # Create reader object by passing the file 
    # object to reader method
    reader_obj = csv.reader(file_obj)
    header = next(reader_obj)
    counter = 1
    # Iterate over each row in the csv 
    # file using reader object
    for row in reader_obj:
        from_email = Email("from_email@domain.com")  # Change to your verified sender
        email = row[3]
        to_email = To(email)  # Change to your recipient
        subject = "Thank you for making the map ausome!"
        firstname = row[0]
        lastname = row[2]
        contentText = "<html><head></head><body><p>Hello, {}</p><br><p>Thank you again for joining us in our goal of making the map ausome!</p><p>We hope that you will continue to take action in making the world more inclusive.</p><p>If you are interested to join us as a volunteer, kindly message us on <a href='https://www.facebook.com/ausomemaps'>facebook</a> or reply to this email.</p><br><p>Cheers,</p><p>Ausome Maps Team</p></body></html>".format(firstname)
        content = Content("text/html", contentText)
        mail = Mail(from_email, to_email, subject, content)

        file_path = 'folder/file-name-{}.pdf'.format(counter) #Change to batch email attachment
        counter = counter + 1

        print(firstname, lastname, email,file_path)
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
            encoded = base64.b64encode(data).decode()
            attachment = Attachment()
            attachment.file_content = FileContent(encoded)
            attachment.file_type = FileType('application/pdf')
            attachment.file_name = FileName('{}_{}.pdf'.format(firstname.replace(" ", ""),lastname.replace(" ", "")))
            attachment.disposition = Disposition('attachment')
            mail.attachment = attachment
            try:
                sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sendgrid_client.send(mail)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)