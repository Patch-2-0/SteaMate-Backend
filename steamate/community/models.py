from django.db import models

# Create your models here.
class Community(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="community")
    