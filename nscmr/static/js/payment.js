angular.module('angularApp')
.controller('PagSeguroController', ["$scope", "$http", "paymentService", "cartService", function($scope, $http, paymentService, cartService) {
  $scope.paymentService = paymentService;
  $scope.cartService = cartService;
  $scope.availableInstallments = null;

  $scope.checkCvv = function() {
    if($scope.paymentService.card.brandInfo.config != undefined) {
      window.brandInfo = $scope.paymentService.card.brandInfo;
      window.card = $scope.paymentService.card;
      if($scope.paymentService.card.cvv.length != $scope.paymentService.card.brandInfo.cvvSize) {
        $scope.paymentForm.cardCvv.$setValidity("size", false);
      } else {
        $scope.paymentForm.cardCvv.$setValidity("size", true);
      }
    }
  };

  $scope.checkNumberSize = function() {
    if($scope.paymentService.card.number.length < 6) {
      $scope.paymentForm.cardNumber.$setValidity("size", false);
    } else if($scope.paymentService.card.brandInfo.config != undefined) {
      if($scope.paymentService.card.brandInfo.config.acceptedLengths.indexOf($scope.paymentService.card.number.length) != -1) {
        $scope.paymentForm.cardNumber.$setValidity("size", true);
      } else {
        $scope.paymentForm.cardNumber.$setValidity("size", false);
      }
    }
  };

  $scope.checkNumber = function() {
    if($scope.paymentService.availableCards === null) getAvailableCards();
    console.log($scope.paymentService.card.number.length);
    if($scope.paymentService.card.brandInfo != null &&
        $scope.paymentService.card.number.length < 6) {
      $scope.paymentService.card.brandInfo = null;
      $scope.availableInstallments = null;
    }
    else if($scope.paymentService.card.number.length >= 6 &&
        $scope.paymentService.card.brandInfo == null) {
      PagSeguroDirectPayment.getBrand({
        cardBin: $scope.paymentService.card.number,
        success: function(response) {
          console.log(response);
          $scope.paymentService.card.brandInfo = response.brand;
          $scope.$apply(function () {
            $scope.paymentService.card.brandInfo.img = getImgSrc(response.brand.name);
          });
          $scope.paymentForm.cardNumber.$setValidity("bin", true);
          checkPaymentOptions();
        },
        error: function(response) {
          console.log(response);
          $scope.paymentForm.cardNumber.$setValidity("bin", false);
        },
        complete: function(response) {
          console.log($scope.paymentForm);
        }
      });
    }
  };

  function getImgSrc(cardType) {
    var rootPath = 'https://stc.pagseguro.uol.com.br';
    if(cardType != undefined) {
      return rootPath +
        $scope.paymentService.availableCards[cardType.toUpperCase()].images.SMALL.path;
    }
    else return;
  };

  function getAvailableCards() {
    $scope.paymentService.availableCards = {};
    PagSeguroDirectPayment.getPaymentMethods({
      success: function(response) {
        console.log(response);
        $scope.paymentService.availableCards = response['paymentMethods']['CREDIT_CARD']['options'];
      },
      error: function(response) {
        console.log(response);
      },
      complete: function(response) {
        console.log(response);
      }
    });
  };


  $scope.checkDate = function(evt) {
    var target = evt.target;
    if(target.value.length == 2) {
      if(target.name === 'cardMonth') {
        if(parseInt(target.value) > 12 || parseInt(target.value) === 0) {
          $scope.paymentForm.cardMonth.$setValidity("outOfRange", false);
        } else {
          $scope.paymentForm.cardMonth.$setValidity("outOfRange", true);
        }
      } else {
        if(parseInt(target.value) < 16) {
          $scope.paymentForm.cardYear.$setValidity("outOfRange", false);
        } else {
          $scope.paymentForm.cardYear.$setValidity("outOfRange", true);
        }
      }
    }
  };

  $scope.getAddressByCep = function() {
    var apiUri = 'http://api.postmon.com.br/v1/cep/' + $scope.paymentService.card.address.zip_code;
    $http({url:apiUri}).then(function success(response) {
      $scope.paymentService.card.address.street_address_1 = response.data['logradouro'];
      $scope.paymentService.card.address.neighbourhood = response.data['bairro'];
      $scope.paymentService.card.address.city = response.data['cidade'];
      $scope.paymentService.card.address.state = response.data['estado'];
    }, function error(response) {
      console.log(response);
      //alert(response.statusText);
      if ($scope.form_errors['zip_code'] === undefined) $scope.form_errors['zip_code'] = [];
      $scope.form_errors['zip_code'].push(response.statusText);
    });
  };


  function checkPaymentOptions() {
    PagSeguroDirectPayment.getInstallments({
      amount: $scope.cartService.cart.total,
      //maxInstallmentsNoInterest: 12,
      brand: $scope.paymentService.card.brandInfo.name,
      success: function(response) {
        $scope.$apply(function() {
          $scope.availableInstallments = response.installments[$scope.paymentService.card.brandInfo.name];
          $scope.installments = $scope.availableInstallments[0];
        });
      },
      error: function(response) {},
      complete: function(response) {
        console.log(response);
      }
    });
  };

}]);

