from django.db import models

# Create your models here.
class UniversityLecture(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    course_url = models.CharField(max_length=255)
    course_school = models.CharField(max_length=255, blank=True, null=True)
    course_teacher = models.CharField(max_length=255, blank=True, null=True)
    course_data = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'University_Lecture'
