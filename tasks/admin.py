from django.contrib import admin
from .models import Project, Task, Staff, ProjectStaff
from mptt.admin import MPTTModelAdmin



# Register your models here.
admin.site.register(Project)
admin.site.register(Task, MPTTModelAdmin)
admin.site.register(Staff)
admin.site.register(ProjectStaff)



# END
