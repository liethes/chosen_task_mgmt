from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
import json, datetime, logging, random
from tasks.models import *



logger = logging.getLogger('default')



#### 文件上传 ####
def uploader(request):
	return render(request, 'uploader.html')



def uploader_addFile(request):
	fileObj = request.FILES.get('file', None)

	origFileName = fileObj.name
	origExt = origFileName.split('.')[1]
	fileName = 'tasks/static/uploaded/uploaded_%d' % random.randint(0, 1000000000) + '.' + origExt  # 不能使用文件名称，因为存在中文，会引起内部错误 # TODO: 改为GUID

	dest = open(fileName, 'wb+')
	dest.write(fileObj.read())
	dest.close()

	return HttpResponse(fileName)



#### 实用函数 ####
def logIt(info):
	logFile = open('myLog_views.log', 'a')
	logFile.write(info + '\n')
	logFile.close()



# 工具函数: 转化任务状态为中文
def xlatTaskStatusCode(code):
	rslt = ''
	if code == 'NEW':
		rslt = ['新发布', '']
	if code == 'ACCEPTED':
		rslt = ['已接受', 'lightyellow']
	if code == 'SUBMITTED':
		rslt = ['已提交', 'yellow']
	if code == 'APPROVED':
		rslt = ['已通过', 'lightgreen']
	if code == 'REJECTED':
		rslt = ['被退回', 'red']
	return rslt



#### 登录模块 ####
# 登入DEMO
def loginDemo(request):
	return render(request, 'login.html')



# 登入
def login(request):
	username = request.GET['username']

	res = HttpResponseRedirect('/')
	res.set_cookie('username', username)

	return res



# 登出
def logout(request):
	res = HttpResponse('已登出' + "<div><a href='/demo'>返回演示页面</a></div>")

	res.delete_cookie('username')

	return res



# 工具函数: 检查用户是否登录
def checkLoginStatus(request):
	username = request.COOKIES.get('username', '')

	if username == '':
		raise OSError('用户没有登录')

	return username



# 工具函数: 根据username获取staff
def getStaffByUserName(userName):
	userId = User.objects.get(username=userName).id
	staff = Staff.objects.get(user_id=userId)
	return staff



#### 首页 ####
# 首页的UI
def home(request):
	username = checkLoginStatus(request)

	return render(request, 'homepage.html', {'username': username})



# 首页的数据
def homepage_data(request):
	username = checkLoginStatus(request)
	staffId = getStaffByUserName(username).id

	projectId = ''
	projectName = ''
	if request.GET.__contains__('projectId'):
		projectId = request.GET['projectId']
		projectName = Project.objects.get(id=projectId).name

	projectList = []
	for project in Project.objects.all():
		projectList.append({
			'id': project.id,
			'name': project.name,
			'desc': project.desc
		})

	taskList = []
	if projectId != '':
		taskObjList = Task.objects.filter(owner_id=staffId, project_id=projectId, status__in=['NEW', 'ACCEPTED', 'REJECTED'])
	else:
		taskObjList = Task.objects.filter(owner_id=staffId, status__in=['NEW', 'ACCEPTED', 'REJECTED'])

	for task in taskObjList:
		taskType = ""
		if task.type == 'MAT':
			taskType = '素材类'
		elif task.type == 'CAM':
			taskType = '镜头类'

		taskImgJson = []
		for taskImg in TaskImg.objects.filter(task_id=task.id):
			taskImgJson.append(taskImg.imgUrl)

		taskList.append({
			'id': task.id,
			'name': task.name,
			'desc': task.desc,
			'type': taskType,
			'beginDate': task.bgn_date.__str__(),
			'endDate': task.end_date.__str__(),
			'projectId': task.project.id,
			'projectName': task.project.name,
			'status': task.status,
			'statusDesc': xlatTaskStatusCode(task.status),
			'imgList': taskImgJson
		})

	curProjectInfo = {
		'id': projectId,
		'name': projectName
	}

	data = {}
	data['curProjectInfo'] = curProjectInfo
	data['projectList'] = projectList
	data['taskList'] = taskList

	return HttpResponse(json.dumps(data), content_type='application/json')



# 创建新项目
def createProject(request):
	name = request.GET['name']
	desc = request.GET['desc']

	project = Project.objects.create(
		name=name,
		desc=desc
	)
	project.save()

	result = {
		'result': 'DONE',
		'detail': {
			'projectId': project.id
		}
	}

	# 返回结果
	return HttpResponse(json.dumps(result), content_type='application/json')



# 甘特图
def gantt(request):
	projectId = request.GET['projectId']
	logger.debug(projectId)
	return render(request, 'gantt.html', {'nodes': Task.objects.all()})



# 函数: 为任务添加图片
def addTaskImg(request, taskObj):
	if request.POST.__contains__('fileList'):
		fileList = request.POST['fileList']
		fileArray = fileList.split('$$$')
		for file in fileArray:
			if file != '':
				taskImgObj = TaskImg.objects.create(
					task=taskObj,
					imgUrl=file
				)
				taskImgObj.save()



# 甘特图的数据
def gantt_data(request):
	# 参数
	projectId = ''
	mode = ''

	if request.method == 'GET':
		projectId = request.GET['projectId']
		mode = request.GET['mode']
	if request.method == 'POST':
		projectId = request.POST['projectId']
		mode = request.POST['mode']
	logger.debug(projectId + ': ' + mode)

	# 返回值
	result = {}

	# 分支: 获取初始化数据
	if mode == 'GET_ALL_DATA':
		result['projectId'] = projectId
		result['projectName'] = Project.objects.get(id=projectId).name

		calBgnDate = datetime.datetime.strptime('2015-09-01', '%Y-%m-%d').date()  # TODO: 去掉HARDCODE
		calEndDate = datetime.datetime.strptime('2015-10-30', '%Y-%m-%d').date()  # TODO: 去掉HARDCODE
		result['calBgnDateStr'] = calBgnDate.strftime('%Y-%m-%d')
		result['calEndDateStr'] = calEndDate.strftime('%Y-%m-%d')

		taskList = []
		taskListInDB = Task.objects.filter(project_id=projectId)
		for oneTaskInDB in taskListInDB:
			oneTask = {}

			oneTask['id'] = oneTaskInDB.id
			oneTask['name'] = oneTaskInDB.name
			oneTask['desc'] = oneTaskInDB.desc
			oneTask['type'] = oneTaskInDB.type
			oneTask['level'] = oneTaskInDB.level
			oneTask['bgnDateStr'] = oneTaskInDB.bgn_date.strftime('%Y-%m-%d')
			oneTask['endDateStr'] = oneTaskInDB.end_date.strftime('%Y-%m-%d')
			oneTask['durationDays'] = (oneTaskInDB.end_date - oneTaskInDB.bgn_date).days + 1
			oneTask['offsetDays'] = (oneTaskInDB.bgn_date - calBgnDate).days
			if oneTaskInDB.owner == None:
				oneTask['owner'] = 0
				oneTask['ownerName'] = ''
			else:
				oneTask['owner'] = oneTaskInDB.owner.id
				oneTask['ownerName'] = Staff.objects.get(id=oneTaskInDB.owner.id).name
			oneTask['status'] = oneTaskInDB.status
			oneTask['statusDesc'] = xlatTaskStatusCode(oneTaskInDB.status)

			taskList.append(oneTask)

		result['taskList'] = taskList

		staffList = []
		prjStaffObj = ProjectStaff.objects.filter(project=projectId)
		for oneStaff in prjStaffObj:
			staffList.append({'id': oneStaff.staff.id, 'name': oneStaff.staff.name})
		result['staffList'] = staffList

	# 分支: 创建任务
	if mode == 'CREATE_TASK':
		parentTask = None
		owner = None

		parentTaskId = request.POST['parentTaskId']
		if parentTaskId != '0':
			parentTask = Task.objects.get(id=parentTaskId)

		ownerId = request.POST['owner']
		if ownerId != '' and ownerId != '0':
			owner = Staff.objects.get(id=ownerId)

		taskObj = Task.objects.create(
			project=Project.objects.get(id=projectId),
			name=request.POST['name'],
			desc=request.POST['desc'],
			type=request.POST['type'],
			bgn_date=datetime.datetime.strptime(request.POST['bgnDateStr'], '%Y-%m-%d').date(),
			end_date=datetime.datetime.strptime(request.POST['endDateStr'], '%Y-%m-%d').date(),
			parent_task=parentTask,
			owner=owner
		)

		taskObj.save()

		# 保存任务附件
		addTaskImg(request, taskObj)

		# 为CAM类任务, 创建默认的子任务
		if request.POST['type'] == 'CAM':
			for subType in ['LAYOUT', '动画', '特效', '解算', '灯光', '合成']:
				subTaskObj = Task.objects.create(
					project=Project.objects.get(id=projectId),
					name=request.POST['name'] + ': ' + subType,
					desc=request.POST['desc'],
					type=subType,
					bgn_date=datetime.datetime.strptime(request.POST['bgnDateStr'], '%Y-%m-%d').date(),
					end_date=datetime.datetime.strptime(request.POST['endDateStr'], '%Y-%m-%d').date(),
					parent_task=taskObj
				)
				subTaskObj.save()

		result = {
			'result': 'DONE',
			'detail': {
				'name': taskObj.name
			}
		}

	# 分支: 修改任务
	if mode == 'MODIFY_TASK':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)

		taskObj.name = request.POST['name']
		taskObj.type = request.POST['type']
		taskObj.desc = request.POST['desc']
		taskObj.bgn_date = datetime.datetime.strptime(request.POST['bgnDateStr'], '%Y-%m-%d').date()
		taskObj.end_date = datetime.datetime.strptime(request.POST['endDateStr'], '%Y-%m-%d').date()
		taskObj.status = request.POST['status']

		owner = None
		ownerId = request.POST['owner']
		if ownerId != '' and ownerId != '0':
			owner = Staff.objects.get(id=ownerId)
		taskObj.owner = owner

		taskObj.save()

		# 保存任务附件
		addTaskImg(request, taskObj)

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 分支: 修改任务时间
	if mode == 'MODIFY_TASK_DATE':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)

		taskObj.bgn_date = datetime.datetime.strptime(request.POST['bgnDateStr'], '%Y-%m-%d').date()
		taskObj.end_date = datetime.datetime.strptime(request.POST['endDateStr'], '%Y-%m-%d').date()

		taskObj.save()

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 分支: 删除任务
	if mode == 'DELETE_TASK':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)
		taskObj.delete()

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 分支: 接受任务（用于首页）
	if mode == 'ACCEPT_TASK':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)
		taskObj.status = 'ACCEPTED'
		taskObj.save()

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 分支: 提交任务（用于首页）
	if mode == 'SUBMIT_TASK':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)
		taskObj.status = 'SUBMITTED'
		taskObj.save()

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 分支: 通过任务（用于任务审批）
	if mode == 'APPROVE_TASK':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)
		taskObj.status = 'APPROVED'
		taskObj.save()

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 分支: 退回任务（用于任务审批）
	if mode == 'REJECT_TASK':
		taskId = request.POST['id']
		taskObj = Task.objects.get(id__exact=taskId)
		taskObj.status = 'REJECTED'
		taskObj.save()

		result = {
			'result': 'DONE',
			'detail': {
				'taskId': taskObj.id
			}
		}

	# 返回结果
	return HttpResponse(json.dumps(result), content_type='application/json')



# My Cam
def myCam(request):
	return render(request, 'myCam.html')



# My Cam的数据
def myCam_data(request):
	projectId = request.GET['projectId']

	result = {}
	result['projectId'] = projectId
	result['projectName'] = Project.objects.get(id=projectId).name

	camList = []
	camListObj = Task.objects.filter(project_id=projectId, type='CAM')
	for camObj in camListObj:
		oneCam = {}
		oneCam['name'] = camObj.name
		oneCam['picUrl'] = 'xxx'
		subTaskObjList = Task.objects.filter(project_id=projectId, parent_task_id=camObj.id)
		for subTaskObj in subTaskObjList:
			if subTaskObj.status == 'NEW':
				oneCam[subTaskObj.type] = 'white'
			if subTaskObj.status == 'ACCEPTED':
				oneCam[subTaskObj.type] = 'lightyellow'
			if subTaskObj.status == 'SUBMITTED':
				oneCam[subTaskObj.type] = 'yellow'
			if subTaskObj.status == 'APPROVED':
				oneCam[subTaskObj.type] = 'lightgreen'
		camList.append(oneCam)
	result['camList'] = camList

	return HttpResponse(json.dumps(result), content_type='application/json')



# END
