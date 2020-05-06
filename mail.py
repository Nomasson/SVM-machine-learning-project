# A function that sends the email of the result to hadas.c@velismedia.com.
import smtplib
def sendemail(message):
    from_addr = 'hopetoworkforyou@gmail.com'
    subject = 'Finished The Program'
    login = 'hopetoworkforyou'
    password = 'velismedia'
    recipient = "hadas.c@velismedia.com"

    # establishing new session
    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.ehlo()
    session.starttls()

    # logging in
    session.login(login, password)
    headers = "\r\n".join(["from: " + from_addr,
                           "subject: " + subject,
                           "to: " + recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])

    # assigning the message (received parameter) to the body of the mail
    body_of_email = message
    content = headers + "\r\n\r\n" + body_of_email
    session.sendmail(login, recipient, content)

    # terminating the session
    session.quit()


