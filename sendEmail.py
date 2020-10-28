import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
emailpasswd = 'drjhlxyvwkzfpdrr'
uname = 'dashealthcare007@gmail.com'

class EmailSender:

    def send_email_to_student(self, recepient_email, message):
        try:
            #self.config_reader=ConfigReader()
            #self.configuration=self.config_reader.read_config()

            # instance of MIMEMultipart
            self.msg = MIMEMultipart()

            # storing the senders email address
            #self.msg['From'] = self.configuration['SENDER_EMAIL']
            self.msg['From'] = uname
            # storing the receivers email address
            self.msg['To'] = ",".join(recepient_email)


            # storing the subject
            self.msg['Subject'] = "Hello"

            # string to store the body of the mail
            #body = "This will contain attachment"
            body=message

            # attach the body with the msg instance
            self.msg.attach(MIMEText(body, 'plain'))


            # instance of MIMEBase and named as p
            self.p = MIMEBase('application', 'octet-stream')


            # creates SMTP session
            self.smtp = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            self.smtp.starttls()

            # Authentication
            self.smtp.login(self.msg['From'], emailpasswd )

            # Converts the Multipart msg into a string
            self.text = self.msg.as_string()

            # sending the mail
            self.smtp.sendmail(self.msg['From'] , recepient_email, self.text)



            # terminating the session
            self.smtp.quit()
        except Exception as e:
            print('the exception is '+str(e))

    def send_email_to_support(self,cust_name,cust_email,cust_contact,course_name,body):
            try:
                

                # instance of MIMEMultipart
                self.msg = MIMEMultipart()

                # storing the senders email address
                self.msg['From'] = uname


                # storing the subject
                self.msg['Subject'] = "DasHealth , Appointment booking"

                # string to store the body of the mail
                # body = "This will contain attachment"

                body = body.replace('cust_name',cust_name)
                body = body.replace('cust_contact', cust_contact)
                body = body.replace('cust_email', cust_email)
                body = body.replace('course_name', course_name)

                # attach the body with the msg instance
                self.msg.attach(MIMEText(body, 'plain'))

                # instance of MIMEBase and named as p
                self.p = MIMEBase('application', 'octet-stream')


                # creates SMTP session
                self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
                self.smtp.ehlo()
                # start TLS for security
                self.smtp.starttls()

                # Authentication
                self.smtp.login(self.msg['From'], emailpasswd)

                # Converts the Multipart msg into a string
                self.text = self.msg.as_string()

                # sending the mail

                self.support_team_email = uname

                self.smtp.sendmail(self.msg['From'], self.support_team_email, self.text)

                # terminating the session
                self.smtp.quit()
            except Exception as e:
                print('the exception is ' + str(e))



