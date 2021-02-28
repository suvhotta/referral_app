from referral.models import Referral, Wallet
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class CreateReferral():
    """
    Creates new referral record for every user who has been referred.
    """

    def __init__(self, referred_by, referred_to):
        self.referred_by = referred_by
        self.referred_to = referred_to

    def new_referral(self):
        Referral.objects.create(referred_by=self.referred_by, referred_to=self.referred_to)


class SendReferral():
    """
    Sends a referral code to the given mail.
    """
    register_page = 'abc@abc.com'

    def __init__(self, mail_id, referral_code):
        self.mail_id = mail_id
        self.referral_code = referral_code

    def send_referral_mail(self):
        message = Mail(
            from_email=os.environ.get('gmail_usr'),
            to_emails=self.mail_id,
            subject='Referral Code to Signup',
            html_content=f'Please register to {SendReferral.register_page} using the code <strong>{self.referral_code}</strong>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            raise e

