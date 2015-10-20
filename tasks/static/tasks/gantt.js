/**
 * Created by TANG on 15-07-30.
 */

//######## 全局变量/函数 ################################################################
var config = {
	taskDivWidth: 20,
	inDebugMode: false
};

var global_projectId = location.href.split('projectId=')[1];
var global_findScopeTaskById;
var global_scopeCurTask;
var global_sendDataBackFunc;

var curTaskDiv = {
	bgnPos: 0, endPos: 0, daysMoved: 0,
	newLen: 0, newDurDays: 0
};



//######## 实用函数 ################################################################
// 函数: 打开【任务详情对话框】
var global_openTaskDetailDialog = function () {
	$('#taskDetailDialog').dialog('open');
};



// 函数: 关闭【任务详情对话框】
var global_closeTaskDetailDialog = function () {
	$('#taskDetailDialog').dialog('close');
};



// 函数: 设置任务行
var global_setupTaskRow = function () {
	// mouseover效果
	$('.taskRow').hover(function () {
		$(this).css('background-color', '#EEE');

		var taskId = $(this).attr('id').replace('ganttCell_taskInfo_row_', '');
		$('#ganttCell_taskDiv_row_' + taskId).css('background-color', '#EEE');
	}, function () {
		$(this).css('background-color', '');

		var taskId = $(this).attr('id').replace('ganttCell_taskInfo_row_', '');
		$('#ganttCell_taskDiv_row_' + taskId).css('background-color', '');
	});

	$('.taskDivRow').hover(function () {
		$(this).css('background-color', '#EEE');

		var taskId = $(this).attr('id').replace('ganttCell_taskDiv_row_', '');
		$('#ganttCell_taskInfo_row_' + taskId).css('background-color', '#EEE');
	}, function () {
		$(this).css('background-color', '');

		var taskId = $(this).attr('id').replace('ganttCell_taskDiv_row_', '');
		$('#ganttCell_taskInfo_row_' + taskId).css('background-color', '');
	});

	// 【任务名称】的Tooltip
	$('.ganttCell_name_innerDiv').tooltip({
		show: 500
	});

	// 【任务状态】单元格
	$('.ganttCell_status').hover(function () {
		if ($(this).attr('data-status') == 'SUBMITTED') {
			$(this).css('cursor', 'pointer');
			$(this).css('background-color', 'red');
			$(this).css('color', 'white')
		}
	}, function () {
		if ($(this).attr('data-status') == 'SUBMITTED') {
			$(this).css('background-color', 'yellow');
			$(this).css('color', '')
		}
	});
};



// 函数: 设置任务Div
var global_setupTaskDivs = function () {
	var $ganttCell_taskDiv = $('.ganttCell_taskDiv');

	// 大小和位置
	$ganttCell_taskDiv.each(function () {
		var thisOffsetDays = parseInt($(this).attr('data-offsetDays'));
		var thisDurationDays = parseInt($(this).attr('data-durationDays'));

		$(this).css('left', thisOffsetDays * config.taskDivWidth);
		$(this).css('width', thisDurationDays * config.taskDivWidth - 1);
	});

	// 可拖放
	$ganttCell_taskDiv.draggable({
		axis: 'x',
		grid: [20, 20],
		start: function (event, ui) {
			curTaskDiv.bgnPos = parseInt(ui.position.left);
		},
		stop: function (event, ui) {
			curTaskDiv.endPos = parseInt(ui.position.left);
			curTaskDiv.daysMoved = (curTaskDiv.endPos - curTaskDiv.bgnPos) / config.taskDivWidth;

			// 修改$scope.taskList中的数据
			var taskId = $(this).attr('id').replace('taskDiv_', '');
			var theTask = global_findScopeTaskById(taskId);

			theTask.offsetDays += curTaskDiv.daysMoved;

			var bgnDate = moment(theTask.bgnDateStr);
			var endDate = moment(theTask.endDateStr);
			var newBgnDate = bgnDate.add(curTaskDiv.daysMoved, 'days');
			var newEndDate = endDate.add(curTaskDiv.daysMoved, 'days');

			theTask.bgnDateStr = newBgnDate.format('YYYY-MM-DD');
			theTask.endDateStr = newEndDate.format('YYYY-MM-DD');

			// 修改$scope.curTask
			global_scopeCurTask.id = taskId;
			global_scopeCurTask.bgnDateStr = theTask.bgnDateStr;
			global_scopeCurTask.endDateStr = theTask.endDateStr;

			global_scopeCurTask.mode = 'MODIFY_TASK_DATE';
			global_scopeCurTask.projectId = global_projectId;

			// 向后端发送
			global_sendDataBackFunc();
		}
	});

	// 可resize
	$ganttCell_taskDiv.resizable({
		handles: 'w,e',
		grid: [20, 20],
		stop: function (event, ui) {
			curTaskDiv.newLen = parseInt($(this).css('width')) + 1;
			curTaskDiv.newDurDays = curTaskDiv.newLen / config.taskDivWidth;

			// 修改$scope.taskList中的数据
			var taskId = $(this).attr('id').replace('taskDiv_', '');
			var theTask = global_findScopeTaskById(taskId);

			theTask.durationDays = curTaskDiv.newDurDays;

			var bgnDate = moment(theTask.bgnDateStr);
			var newEndDate = bgnDate.add(curTaskDiv.newDurDays - 1, 'days');

			theTask.endDateStr = newEndDate.format('YYYY-MM-DD');

			// 修改$scope.curTask
			global_scopeCurTask.id = taskId;
			global_scopeCurTask.bgnDateStr = theTask.bgnDateStr;
			global_scopeCurTask.endDateStr = theTask.endDateStr;

			global_scopeCurTask.mode = 'MODIFY_TASK_DATE';
			global_scopeCurTask.projectId = global_projectId;

			// 向后端发送
			global_sendDataBackFunc();
		}
	});

	// mouseover效果
	$ganttCell_taskDiv.hover(function () {
		$(this).css('opacity', 0.5);
	}, function () {
		$(this).css('opacity', 1);
	})
};



//######## Angular专有处理内容 ################################################################
var app = angular.module('ganttApp', []);



// 特殊处理: 解决angular的post和dJango不兼容的问题
app.config(['$httpProvider', function ($httpProvider) {
	// setup CSRF support
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	// Rewrite POST body data
	$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
	// Override $http service's default transformRequest
	$httpProvider.defaults.transformRequest = [function (data) {
		/**
		 * The workhorse; converts an object to x-www-form-urlencoded serialization.
		 * @param {Object} obj
		 * @return {String}
		 */
		var param = function (obj) {
			var query = '';
			var name, value, fullSubName, subName, subValue, innerObj, i;

			for (name in obj) {
				value = obj[name];

				if (value instanceof Array) {
					for (i = 0; i < value.length; ++i) {
						subValue = value[i];
						fullSubName = name + '[' + i + ']';
						innerObj = {};
						innerObj[fullSubName] = subValue;
						query += param(innerObj) + '&';
					}
				}
				else if (value instanceof Object) {
					for (subName in value) {
						subValue = value[subName];
						fullSubName = name + '[' + subName + ']';
						innerObj = {};
						innerObj[fullSubName] = subValue;
						query += param(innerObj) + '&';
					}
				}
				else if (value !== undefined && value !== null) {
					query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
				}
			}

			return query.length ? query.substr(0, query.length - 1) : query;
		};

		return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
	}];
}
]);



// Angular控制器定义
app.controller('ganttCtrl', function ($scope, $http) {
	// 基础变量
	$scope.cfg_taskDivWidth = config.taskDivWidth;

	$scope.projectId = global_projectId;

	$scope.curTask = {};
	global_scopeCurTask = $scope.curTask;

	$scope.taskTypeArray = [
		{name: 'MAT', desc: '素材'},
		{name: 'CAM', desc: '镜头'}
	];

	$scope.taskStatusArray = ['NEW', 'ACCEPTED', 'SUBMITTED', 'APPROVED', 'CANCELED'];

	$scope.staffList = [];

	$scope.findTaskById = function (taskId) {
		for (var i = 0; i < $scope.taskList.length; i++) {
			if ($scope.taskList[i].id == taskId) {
				return $scope.taskList[i];
			}
		}
	};
	global_findScopeTaskById = $scope.findTaskById;



	// 初始化: 获取任务数据 & 设置UI
	$http.get('/gantt/data?mode=GET_ALL_DATA&projectId=' + global_projectId)
		.success(function (data, header, config, status) {
			// 数据: 项目信息
			$scope.projectName = data.projectName;

			// 数据: 任务
			$scope.taskList = data.taskList;

			// 数据: 日期
			$scope.calBgnDateStr = data.calBgnDateStr;
			$scope.calEndDateStr = data.calEndDateStr;

			var calBgnDate = moment(data.calBgnDateStr);
			var calEndDate = moment(data.calEndDateStr);
			$scope.dayCount = calEndDate.diff(calBgnDate, 'days') + 1;
			$scope.dateList = [];
			for (var i = 0; i < $scope.dayCount; i++) {
				var theDate = moment(data.calBgnDateStr).add(i, 'days'); // 注意: 此处不能用calBgnDate.add(i, 'days'), 会出现奇怪的情况
				var theMon = theDate.format('M');
				var theDay = theDate.format('D');
				$scope.dateList.push([theMon, theDay]);
			}

			// 数据: 人员
			$scope.staffList = data.staffList;

			// 一些延时处理
			setTimeout(function () {
				global_setupTaskRow();
				global_setupTaskDivs();
			}, 100)
		});



	// 动作: 新增任务
	$scope.createOneTask = function (taskId) {
		$scope.curTask.mode = 'CREATE_TASK';
		$scope.curTask.projectId = $scope.projectId;

		$scope.curTask.parentTaskId = taskId;
		$scope.curTask.name = '';
		$scope.curTask.type = 'MAT';
		$scope.curTask.desc = '';
		$scope.curTask.bgnDateStr = '2015-10-01';
		$scope.curTask.endDateStr = '2015-10-01';
		$scope.curTask.owner = '';

		global_openTaskDetailDialog();
	};



	// 动作: 修改任务
	$scope.modifyOneTask = function (taskId) {
		for (var i = 0; i < $scope.taskList.length; i++) {
			if ($scope.taskList[i].id == taskId) {
				$scope.curTask = $.extend({}, $scope.taskList[i]); // 克隆一个对象

				$scope.curTask.mode = 'MODIFY_TASK';
				$scope.curTask.projectId = $scope.projectId;

				global_scopeCurTask = $scope.curTask;

				break;
			}
		}

		global_openTaskDetailDialog();
	};



	// 动作: 删除任务
	$scope.deleteOneTask = function (taskId) {
		var confirmDelete = confirm('确定要删除任务?');

		if (confirmDelete) {
			$scope.curTask.mode = 'DELETE_TASK';
			$scope.curTask.projectId = $scope.projectId;

			$scope.curTask.id = taskId;

			$scope.sendDataBack();
		}
	};



	// 动作: 将数据发回后端
	$scope.sendDataBack = function () {
		console.log('sending data back: ' + JSON.stringify($scope.curTask));

		$('#fileUploadForm').submit();

		$http.post('/gantt/data', $scope.curTask)
			.success(function (data, header, config, status) {
				console.log(JSON.stringify(data));

				location.reload();
			});
	};

	global_sendDataBackFunc = $scope.sendDataBack;



	// #### 函数: 进行任务审批 ####
	$scope.makeTaskApproval = function (taskId) {
		var task = $scope.findTaskById(taskId);

		if (task.status == 'SUBMITTED') {
			var $theDlg = $('#taskApprovalDlg');
			$theDlg.attr('data-taskId', taskId);
			$theDlg.dialog('open');
		}
	};

	// #### 函数: 任务审批 - 通过 ####
	$scope.sendBack_approveTask = function () {
		var taskId = $('#taskApprovalDlg').attr('data-taskId');

		$http.post('/gantt/data', {projectId: global_projectId, id: taskId, mode: 'APPROVE_TASK'})
			.success(function (data, header, config, status) {
				$('#taskApprovalDlg').dialog('close');

				alert('任务已审批通过');

				location.reload();
			});
	};

	// #### 函数: 任务审批 - 退回 ####
	$scope.sendBack_rejectTask = function () {
		var taskId = $('#taskApprovalDlg').attr('data-taskId');

		$http.post('/gantt/data', {projectId: global_projectId, id: taskId, mode: 'REJECT_TASK'})
			.success(function (data, header, config, status) {
				$('#taskApprovalDlg').dialog('close');

				alert('任务已退回');

				location.reload();
			});
	};



	// #### 过滤器 - 显示【待审核任务】 ####
	$scope.filter_showSubmitted = function () {
		$('.taskRow').hide();
		$('.taskDivRow').hide();
		$("tr[data-status='SUBMITTED']").show();
	};

	// #### 过滤器 - 显示【全部任务】 ####
	$scope.filter_showAll = function () {
		$('.taskRow').show();
		$('.taskDivRow').show();
	};



	console.log('angular初始化完毕');



	// 临时测试
	$scope.tempTest = function () {
		var tmpTask = {
			id: 888,
			name: 'fuck',
			type: 'MAT',
			desc: '测试测试测试',
			bgnDateStr: '2015-10-01',
			endDateStr: '2015-10-01',
			durationDays: 1,
			offsetDays: 30,
			level: 2
		};
		$scope.taskList.splice(2, 0, tmpTask);
		//$scope.taskList.push(tmpTask);
	}
});



// #### 函数: 初始化文件uploader ####
var initPlupload = function () {
	var uploader = new plupload.Uploader({
		browse_button: 'browse', // this can be an id of a DOM element or the DOM element itself
		url: '/uploader/add',
		multipart: 'form-data'
	});

	uploader.init();

	uploader.bind('FilesAdded', function (up, files) {
		var html = '';
		plupload.each(files, function (file) {
			html += '<li id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b></li>';
		});
		document.getElementById('fileList').innerHTML += html;
	});

	uploader.bind('UploadProgress', function (up, file) {
		document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
	});

	uploader.bind('Error', function (up, err) {
		document.getElementById('console').innerHTML += "\nError #" + err.code + ": " + err.message;
	});

	uploader.bind('FileUploaded', function (up, file, info) {
		var fileName = info.response.replace('tasks/', '/');
		console.log(fileName);
		$('#fileListServer').append("<li class='serverFile'>" + fileName + "</li>");
	});

	document.getElementById('start-upload').onclick = function () {
		uploader.start();
	};

};



//######## jQuery专有处理内容 ################################################################
$(document).ready(function () {
	$('button').button();

	// 整个日历区域可拖放
	$('#ganttCalendarBody_innerDiv').draggable({
		axis: 'x',
		drag: function (event, ui) {
			$('#ganttCalendarTitle_innerDiv').css('left', ui.position.left);
		}
	});



	// 添加/修改任务对话框
	$.datepicker.setDefaults({
		dayNamesMin: ['日', '一', '二', '三', '四', '五', '六'],
		dateFormat: 'yy-mm-dd'
	});
	$('#tadkInfoDlg_bgnDate').datepicker();
	$('#tadkInfoDlg_endDate').datepicker();



	// 延时器
	var doSomeStuff = function () {
		// UI初始化: 任务详情对话框
		$('#taskDetailDialog').dialog({
			autoOpen: false,
			width: 640,
			height: 400,
			modal: true,
			buttons: [
				{
					text: '确定',
					click: function () {
						// 记录server file list
						var serverFileList = '';
						$('.serverFile').each(function () {
							serverFileList += $(this).text() + '$$$';
						});
						console.log(serverFileList);
						global_scopeCurTask['fileList'] = serverFileList;

						$('#fileList').empty();
						$('#fileListServer').empty();

						// 向后端发数据
						global_sendDataBackFunc();

						$(this).dialog('close');
					}
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

		// UI初始化: 任务审核对话框
		$('#taskApprovalDlg').dialog({
			autoOpen: false,
			width: 300,
			height: 110,
			modal: true,
			closeOnEscape: true
		});

		// 视效设置: 任务Action按钮
		$('.taskActionBtn').hover(function () {
			$(this).css('opacity', 0.5);
		}, function () {
			$(this).css('opacity', 1);
		});

		// 初始化文件uploader
		initPlupload();

		//// 设置Tooltip
		//$('.ganttCell_name').tooltip({
		//	position: {my: "left+0 center", at: "right center"},
		//	content: function () {
		//		var taskId = $(this).attr('data-taskId');
		//
		//		var theTip = "";
		//		theTip += "<span style='background-color:green; color:white; font-size:8pt; font-weight:bold; cursor:pointer; padding:0 3px;' onclick='global_createOneTaskFunc(" + taskId + ")'>增</span>&nbsp;";
		//		theTip += "<span style='background-color:red; color:yellow;  font-size:8pt; font-weight:bold; cursor:pointer; padding:0 3px;' onclick='global_deleteOneTaskFunc(" + taskId + ");'>删</span>&nbsp;";
		//		theTip += "<span style='background-color:brown; color:white; font-size:8pt; font-weight:bold; cursor:pointer; padding:0 3px;' onclick='global_modifyOneTaskFunc(" + taskId + ");'>改</span>";
		//
		//		return theTip;
		//	},
		//	show: null,
		//	close: function (event, ui) {
		//		ui.tooltip.hover(function () {
		//				$(this).stop(true).fadeTo(400, 1);
		//			},
		//			function () {
		//				$(this).fadeOut('400', function () {
		//					$(this).remove();
		//				});
		//			});
		//	}
		//});
		//console.log('任务tooltip已经设置');

		console.log('杂项延时处理完毕');
	};
	setTimeout(doSomeStuff, 500);



	console.log('jQuery初始化完毕');
});



// END
