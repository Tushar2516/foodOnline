from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import *
# Create your models here.

# Vendor model....
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.vendor_name
    
    # For accessing the save method while it call for approval to vendor
    def save(self, *args,**kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user':self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved == True:
                    #  Send Notification Email
                    mail_subject = 'Congratulations! Your Restaurant Has Been Approved.'
                    send_notification(mail_subject, mail_template, context)
                else:
                    #  Send Notification email
                    mail_subject = 'Sorry You are not eligible for our website.'
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args,**kwargs)