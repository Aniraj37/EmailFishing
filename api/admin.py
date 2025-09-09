from django.contrib import admin
from .models import EmailScan, FailureEmail

# Register your models here.
# class EmailScan(admin.ModelAdmin):
#     list_display=("setup_file", "email_file")

admin.site.register(EmailScan)
admin.site.register(FailureEmail)
