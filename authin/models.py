from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from myalgs.settings import SECRET_KEY
# Create your models here.
class User(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=100)
    user_pass_hash=models.CharField(max_length=100)
    user_confirmed=models.BooleanField(default=0)
    def generate_confirm_token(self):
        s=Serializer(SECRET_KEY,expires_in=3600)
        return  s.dumps({'confirm_id':self.id})

    def email_confirm(self,token):
        s = Serializer(SECRET_KEY, expires_in=3600)
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm_id') == self.id:
            self.user_confirmed=True
            self.save()
            return True
        return False
