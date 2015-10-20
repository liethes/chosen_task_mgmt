var homepageData;



// #### 函数: 打开【新建项目对话框】 ####
var openNewProjectDialog = function () {
	$('#newProjectDialog').dialog('open');
};



// #### 函数: 创建新项目（新建项目对话框 - 确定） ####
var createProject = function () {
	var name = $('#newProjectDialog_name').val();
	var desc = $('#newProjectDialog_desc').val();

	$.post("/createProject?name=" + name + "&desc=" + desc + "", function (data) {
		// TODO: 转码
		console.log(JSON.stringify(data));

		$('#newProjectDialog').dialog('close');
	});
};



// #### 函数: 接受任务 ####
function acceptTask(projectId, taskId) {
	$.post('gantt/data', {mode: 'ACCEPT_TASK', projectId: projectId, id: taskId})
		.success(function (data) {
			alert('您已接受任务');

			$('#acceptBtn_' + taskId).hide();
		});
}



// #### 函数: 接受任务 ####
function submitTask(projectId, taskId) {
	$.post('gantt/data', {mode: 'SUBMIT_TASK', projectId: projectId, id: taskId})
		.success(function (data) {
			alert('任务已提交审核');

			$('#submitBtn_' + taskId).hide();
		});
}



// #### 函数：渲染一个Task ####
function renderOneTask(taskId) {
	var result = "";
	homepageData.taskList.forEach(function (oneTask) {
		if (oneTask.id == taskId) {
			result += "<table>";
			result += "  <tr valign=top>";
			result += "    <td>";
			if (oneTask.imgList.length > 0) {
				result += "      <img src='" + oneTask.imgList[0] + "' style='width:400px; height:300px;'/>";
			}
			result += "    </td>";
			result += "    <td>";
			result += "      <div>" + oneTask.projectName + "</div>";
			result += "      <div style='font-size:32px; font-weight:bold;'>" + oneTask.name + "</div>";
			result += "      <div>" + oneTask.type + "</div>";
			//result += "      <div style='text-align:right;'>" + oneTask.statusDesc[0] + "</div>";
			result += "      <div style='margin:3px 0; color:#999;'>" + oneTask.desc + "</div>";
			result += "    </td>";
			result += "  </tr>";
			result += "</table>";

			result += "<table width=100%>";
			//result += "<tr><td colspan=2 style='color:#999;'>" + oneTask.desc + "</td></tr>";

			result += "<tr><td>起始日期</td><td>" + oneTask.beginDate + "</td></tr>";
			result += "<tr><td>结束日期</td><td>" + oneTask.endDate + "</td></tr>";

			//result += "<tr><td>任务ID</td><td>" + oneTask.id + "</td></tr>";

			result += "<tr><td colspan=2>&nbsp;</td></tr>";

			result += "<tr>";
			result += "  <td style='text-align:left;'>";
			if (oneTask.status == 'NEW') {
				result += "    <span id='acceptBtn_" + oneTask.id + "' style='background-color:blue; color:white; padding:5px; border-radius:3px; cursor:pointer;' onclick='acceptTask(" + oneTask.projectId + ", " + oneTask.id + ")'>接受任务</span>";
			}
			result += "  </td>";
			result += "  <td style='text-align:right;'>";
			if (oneTask.status == 'ACCEPTED' || oneTask.status == 'REJECTED') {
				result += "    <span id='submitBtn_" + oneTask.id + "' style='background-color:red; color:white; padding:5px; border-radius:3px; cursor:pointer;' onclick='submitTask(" + oneTask.projectId + ", " + oneTask.id + ")'>提交任务</span>";
			}
			result += "  </td>";
			result += "</tr>";
			result += "</table>";
		}
	});
	return result;
}



// #### jQuery处理部分 ####
$(document).ready(function () {
	// 向后端取数据
	var url;
	var curProjectId = location.href.split('projectId=')[1]; // TODO: 改成更好的方式
	if (curProjectId != undefined) {
		url = "/homepage_data" + "?projectId=" + curProjectId;
	} else {
		url = "/homepage_data";
	}

	$.get(url, function (data) {
		homepageData = data;

		// 填数据: 当前project name
		$('#curProjectName').text(homepageData.curProjectInfo.name);

		// 填数据: project list
		homepageData.projectList.forEach(function (oneProject) {
			$('#projectList_seperator').before("<li><a href='?projectId=" + oneProject.id + "'>" + oneProject.name + "</a></li>")
		});

		// 填数据: task list
		$('#taskList').html('');
		homepageData.taskList.forEach(function (oneTask) {
			var html = "";
			html += "<div class='task' id=" + oneTask.id + " style='position:relative;'>";
			html += oneTask.name;

			if (oneTask.status == 'NEW') {
				html += "&nbsp;<span style='background-color:#a6c9e2; color:white; font-size:6pt; position:absolute; right:5px; padding:3px; border-radius:3px;'>(新发布)</span>"
			}
			if (oneTask.status == 'REJECTED') {
				html += "&nbsp;<span style='background-color:red; color:white; font-size:6pt; position:absolute; right:5px; padding:3px; border-radius:3px;'>!被退回!</span>"
			}

			html += "</div>";

			$('#taskList').append(html)
		});

		var $taskItem = $('.task');

		// 设效果 - hover
		$taskItem.hover(function () {
			$(this).addClass('hover');
		}, function () {
			$(this).removeClass('hover');
		});

		// 设效果 - Task.Click：更新任务详情&相关项目
		$taskItem.click(function () {
			var projectId = $(this).attr('data-projectId');
			var taskId = $(this).attr('id');
			$('#taskDetail').html(renderOneTask(taskId));
			$('.task').removeClass('selected');
			$(this).addClass('selected');
		})


	});



	// 美化菜单
	if (curProjectId != undefined) {
		$('#menuItem_toGantt').show().attr('href', '/gantt?projectId=' + curProjectId);
		$('#menuItem_toMyCam').show().attr('href', '/myCam?projectId=' + curProjectId);
	}
	//$('.menuItem').hover(function () {
	//	$(this).addClass('menuItemHover');
	//}, function () {
	//	$(this).removeClass('menuItemHover');
	//});



	// UI设置: 新建项目对话框
	$('#newProjectDialog').dialog({
		autoOpen: false,
		width: 600,
		height: 300,
		modal: true,
		buttons: [
			{
				text: '确定',
				click: createProject
			},
			{
				text: '取消',
				click: function () {
					$(this).dialog('close');
				}
			}
		],
		closeOnEscape: true
	});
});



// END
