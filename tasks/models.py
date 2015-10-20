from django.db import models
from mptt.models import MPTTModel
from django.contrib.auth.models import User, Group



#### 测试: 文件上传 ####
class Camper(models.Model):
	name = models.CharField(max_length=30)
	img = models.FileField(upload_to='./upload')

	def __str__(self):
		return self.name



#### 人员 ####
class Staff(models.Model):
	name = models.CharField(max_length=50, verbose_name='姓名')
	desc = models.CharField(max_length=250, verbose_name='描述', null=True)
	email = models.CharField(max_length=250, verbose_name='电邮', null=True)
	user = models.ForeignKey(User, verbose_name='对应用户', null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = verbose_name_plural = "人员"



#### 项目 ####
class Project(models.Model):
	name = models.CharField(max_length=100, verbose_name='项目名称')
	desc = models.TextField(null=True, verbose_name='详细描述')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = verbose_name_plural = "项目"



#### 项目中的人员 ####
class ProjectStaff(models.Model):
	project = models.ForeignKey(Project, default=0, verbose_name='项目')
	staff = models.ForeignKey(Staff, default=0, verbose_name='人员')

	class Meta:
		verbose_name = verbose_name_plural = '项目人员'



#### 任务 ####
class Task(MPTTModel):
	project = models.ForeignKey(Project, default=0, verbose_name='所属项目')
	name = models.CharField(max_length=100, verbose_name='任务名称')
	type = models.CharField(max_length=4, verbose_name='任务类型', choices=(('CAM', '镜头类'), ('MAT', '素材类')))
	desc = models.TextField(verbose_name='详细描述', null=True)
	bgn_date = models.DateField(verbose_name='开始日期')
	end_date = models.DateField(verbose_name='结束日期')
	sender = models.ForeignKey(Staff, verbose_name='发出人', null=True, blank=True, related_name='sender')
	owner = models.ForeignKey(Staff, verbose_name='制作人', null=True, blank=True, related_name='owner')
	parent_task = models.ForeignKey('self', verbose_name='父任务', null=True, blank=True)
	status = models.CharField(max_length=10, default='NEW', verbose_name='状态')

	class MPTTMeta:
		parent_attr = 'parent_task'

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = verbose_name_plural = "任务"



#### 任务的图片 ####
class TaskImg(models.Model):
	task = models.ForeignKey(Task, verbose_name='所属任务')
	imgUrl = models.CharField(max_length=500, verbose_name='图片url')



# END
