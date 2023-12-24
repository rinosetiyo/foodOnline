from django.db import models
from accounts.models import User, UserProfile
from vendor.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    vendor_name = models.CharField(max_length=200, blank=True)
    vendor_license = models.ImageField(upload_to='vendors/vendor_license', blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            mail_template = 'accounts/emails/admin_approval_email.html'
            context = {
                'user': self.user,
                'is_approved': self.is_approved,
            }
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                if self.is_approved == True:
                    #send notification
                    mail_subject = "congratulation you have been approved"
                    send_notification(mail_subject, mail_template, context)
                else:
                    #send notification
                    mail_subject = "your approval is failed"
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)