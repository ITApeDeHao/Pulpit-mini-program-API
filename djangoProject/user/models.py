from django.db import models

# Create your models here.
class UserInfo(models.Model):
     ID = models.BigAutoField(verbose_name="ID",primary_key=True)
     Phone = models.CharField(verbose_name="手机号", max_length=11, unique=True)
     PassWord = models.CharField(verbose_name="密码",max_length=16)
     token = models.CharField(verbose_name="用户token", max_length=64, null=True, blank=True)
     UserName = models.CharField(verbose_name="用户名", null=True, max_length=255,default="hhhh")
     grade = models.IntegerField(verbose_name="等级",null=False,default=1)
     attentionnum = models.PositiveIntegerField(db_column='AttentionNum',default=0)  # Field name made lowercase.
     resume = models.CharField(db_column='Resume', max_length=255, blank=True, null=True)  # Field name made lowercase.


class UserAttention(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField()
    attention_id = models.IntegerField()
    attention_status = models.IntegerField(blank=True, null=True, choices=[(0,1)], default=1)

    class Meta:
        managed = False
        db_table = 'user_attention'