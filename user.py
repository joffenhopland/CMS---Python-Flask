class User():

    # construct user object to use for flask_login
    def __init__(self, id, firstname, lastname, epost, passwordHash, verifisert, adgang, verifiseringskode):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.epost = epost
        self.passwordHash = passwordHash
        self.verifisert = verifisert
        self.adgang = adgang
        self.verifiseringskode = verifiseringskode
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.epost

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
