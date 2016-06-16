angular.module('angularApp')
.controller("AddressController", ["$scope","$http", "addressesService", function($scope, $http, addressesService) {
  $scope.addressesService = addressesService;
  $scope.form = {};
  $scope.form_errors = {};
  $scope.form_success = '';
  $scope.addAddress = function() {
    $http({
      method: 'POST',
      url: addAddressUri,
      data: $.param($scope.form),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        "X-CSRFToken": csrfToken
      }
    }).then(function successCallback(response) {
      $scope.form_errors = {};
      $scope.form_success = response.data;
      addressesService.update(getAddressesUri);
    }, function errorCallback(response) {
      $scope.form_success = '';
      $scope.form_errors = response.data;
    });
  };

  $scope.getAddressByCep = function() {
    var apiUri = 'http://api.postmon.com.br/v1/cep/' + $scope.form.zip_code;
    $http({url:apiUri}).then(function success(response) {
      $scope.form.street_address_1 = response.data['logradouro'];
      $scope.form.neighbourhood = response.data['bairro'];
      $scope.form.city = response.data['cidade'];
      $scope.form.state = response.data['estado'];
    }, function error(response) {
      console.log(response);
      //alert(response.statusText);
      if ($scope.form_errors['zip_code'] === undefined) $scope.form_errors['zip_code'] = [];
      $scope.form_errors['zip_code'].push(response.statusText);
    });
  };

}]);
