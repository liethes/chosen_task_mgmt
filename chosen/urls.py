"""choose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	# 测试
	url(r'^uploader$', 'tasks.views.uploader'),
	url(r'^uploader/add$', 'tasks.views.uploader_addFile'),

	# 管理界面
	url(r'^admin/', include(admin.site.urls)),

	# 登录
	url(r'^demo', 'tasks.views.loginDemo'),
	url(r'^login$', 'tasks.views.login'),
	url(r'^logout$', 'tasks.views.logout'),

	# 首页
	url(r'^$', 'tasks.views.home', name='home'),
	url(r'^homepage_data$', 'tasks.views.homepage_data'),
	url(r'^createProject$', 'tasks.views.createProject'),

	# 甘特图
	url(r'^gantt$', 'tasks.views.gantt', name='gantt'),
	url(r'^gantt/data$', 'tasks.views.gantt_data', name='gantt_data'),

	# MY CAM
	url(r'^myCam$', 'tasks.views.myCam', name='myCam'),
	url(r'^myCam/data$', 'tasks.views.myCam_data', name='myCam_data'),
]



# END
