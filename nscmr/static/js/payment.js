angular.module('angularApp')
.controller('PagSeguroController', ["$scope", "$http", "paymentService", function($scope, $http, paymentService) {
  $scope.paymentService = paymentService;

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

  $scope.isNumeric = function(evt) {
    var theEvent = evt;
    window.theEvent = theEvent;
    var key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode(key);
    var regex = /[0-9]/;
    if(!regex.test(key)) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
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

}]);

