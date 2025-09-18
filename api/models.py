from django.db import models
import uuid
# Create your models here.
class EmailScan(models.Model):
    '''
    - Stores failed emails and its setup files
    '''
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_column="ID"
    )
    setup_file = models.FileField(upload_to="setup_files/")
    email_file = models.FileField(upload_to="email_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
class FailureEmail(models.Model):
    '''
    - stores details of the flagged emails along with its id
    '''
    email = models.ForeignKey(EmailScan, on_delete=models.CASCADE, related_name="failures")
    phrase = models.CharField(max_length=255)
    start_line = models.IntegerField(null=True, blank=True)
    segment_lines = models.JSONField()
    matched_segments = models.JSONField()
    total_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phrase} in {self.email.email_file}"