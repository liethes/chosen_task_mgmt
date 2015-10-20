var global_projectId = location.href.split('projectId=')[1];



var app = angular.module('myCamApp', []);

app.controller('myCamCtrl', function ($scope, $http) {
	$http.get('/myCam/data' + '?projectId=' + global_projectId)
		.success(function (data, header, config, status) {
			console.log(JSON.stringify(data));

			$scope.projectName = data.projectName;

			$scope.camList = data.camList
		});
});



// END
