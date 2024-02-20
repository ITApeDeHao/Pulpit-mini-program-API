from django.db import models

# Create your models here.

class ForumForummsg(models.Model):
    forum_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    forum_msg = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    intro = models.CharField(max_length=255)
    pageview = models.PositiveIntegerField(default=0)
    spot = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'forum_forummsg'


class ForumComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    forum_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()
    content = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forum_comment'

class ForumSpot(models.Model):
    spotid = models.AutoField(db_column='spotId', primary_key=True)  # Field name made lowercase.
    spot_user_id = models.IntegerField()
    spot_forum_id = models.IntegerField()
    spot_status = models.IntegerField(choices=[(0,1)],default=1)

    class Meta:
        managed = False
        db_table = 'forum_spot'

