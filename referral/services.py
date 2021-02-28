from referral.models import Referral, Wallet

class CreateReferral():
    """
    Creates new referral record for every user who has been referred.
    """

    def __init__(self, referred_by, referred_to):
        self.referred_by = referred_by
        self.referred_to = referred_to

    def new_referral(self):
        Referral.objects.create(referred_by=self.referred_by, referred_to=self.referred_to)

