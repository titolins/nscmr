angular.module('galleryApp', [])
.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}])
/*
.filter("safe", ['$sce', function($sce) {
  return function(htmlCode){
    return $sce.trustAsHtml(htmlCode);
  }
}])
*/
.controller("GalleryController", ["$scope","$http", "$timeout", function($scope, $http, $timeout) {
  $scope.gallery = [];
  $scope.variantImages = {};
  $scope.selectedImages = [];
  $scope.selectedVariantImages = [];
  $scope.updateGallery = function() {
    $http({
      method: 'GET',
      url: getGalleryUri,
      headers: {
        "Accept": "application/json;utf-8"
      }
    }).then(function successCallback(response) {
      console.log(response);
      $scope.gallery = response.data;
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  $scope.selectImage = function(event) {
    event.preventDefault();
    var target = event.target;
    while(!target.classList.contains('img-selector')) {
      target = target.parentNode;
    }
    if(target.classList.contains('selected')) {
      $scope.selectedImages.splice(target.id,1);
    } else {
      $scope.selectedImages.push(target.id);
    }
    target.classList.toggle('selected');
  };

  $scope.selectVariantImage = function(event) {
    event.preventDefault();
    var target = event.target;
    while(!target.classList.contains('img-selector')) {
      target = target.parentNode;
    }
    if(target.classList.contains('selected')) {
      $scope.selectedVariantImages.splice(target.id,1);
    } else {
      $scope.selectedVariantImages.push(target.id);
    }
    target.classList.toggle('selected');
  };

  $scope.removeImages = function(event) {
    var target = event.target;
    while(!target.classList.contains("modal")) target = target.parentNode;
    var variantId = target.id.split('-')[1];
    $http({
      method: 'DELETE',
      url: addImagesUri,
      data: {
        variant_id: variantId,
        imgs: $scope.selectedVariantImages},
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function success(response) {
      console.log(response);
      /*
      $timeout(function() {
        $scope.getVariantImages(variantId);
      }, 1000);
      */
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.addImages = function(event) {
    var target = event.target;
    while(!target.classList.contains("modal")) target = target.parentNode;
    var variantId = target.id.split('-')[1];
    $http({
      method: 'PUT',
      url: addImagesUri,
      data: {
        variant_id: variantId,
        imgs: $scope.selectedImages},
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json;utf-8"
      }
    }).then(function success(response) {
      console.log(response);
      /*
      $timeout(function() {
        $scope.getVariantImages(variantId);
      }, 1000);
      */
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.clearSelection = function() {
    $scope.selectedImages = [];
    $scope.selectedVariantImages = [];
    //img-selector.selected
    var targets = document.getElementsByClassName('img-selector selected');
    for(var i = 0; i < targets.length; i++) {
      targets[i].classList.remove('selected');
    }
  };

  $scope.getVariantImages = function(varId) {
    console.log('ok');
    $http({
      url: addImagesUri + '/' + varId,
      headers: {
        "Accept": "application/json;utf-8"
      }
    }).then(function success(response) {
      $scope.variantImages[varId] = response.data;
      console.log(response);
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.updateGallery();
}]).directive('gallery', function($compile, $timeout) {
  function buildTemplate($scope, varId) {
    var template = '' +
    '<div class="modal-dialog"><div class="modal-content"><div class="modal-header">' +
    '<button type="button" ng-click="clearSelection()" class="close" data-dismiss="modal" arial-label="Fechar">' +
    '<span aria-hidden="true">×</span></button>' +
    '<h4 class="modal-title" id="gallery-title">Galeria de imagens</h4></div>' +
    '<div class="modal-body"><div class="tabpanel"><ul class="nav nav-tabs" role="tablist">' +
    '<li role="presentation" class="active">' +
    '<a href="#variant-imgs" aria-controls="variant-imgs" role="tab" data-toggle="tab" aria-expanded="true">Imagens do produto</a>' +
    '</li><li role="presentation">' +
    '<a href="#img-gallery-pane" aria-controls="img-gallery-pane" role="tab" data-toggle="tab" aria-expanded="true">Galeria de imagens</a>' +
    '</li></ul><div class="tab-content">' +
    '<div id="variant-imgs" role="tabpanel" class="tab-pane img-gallery active">';
    if(varId != "") {
      $scope.variantImages[varId].map(function(p) {
        template += '<a href="#" ng-click="selectVariantImage($event)">' +
          '<div class="col-xs-4 img-selector" id="'+ p["id"]+'">' +
          '<img src="' + p['thumb'] + '" class="img-responsive"></img></div></a>';
      });
      template += '<div class="clearfix"></div>';
    }
    template += '<button ng-click="removeImages($event)" type="button" class="btn btn-primary">Remover fotos do produto</button></div>' +
    '<div id="img-gallery-pane" role="tabpanel" class="tab-pane img-gallery">';
    $scope.gallery.map(function(p) {
      template += '' +
      '<a href="#" ng-click="selectImage($event)">' +
        '<div class="col-xs-4 img-selector" id="'+p["id"]+'">' +
          '<img class="img-responsive" src="'+p['thumb']+'"></img>' +
        '</div>' +
      '</a>';
    });
    template += '' +
      '<div class="clearfix"></div>' +
      '<button ng-click="addImages($event)" type="button" class="btn btn-primary">Adicionar foto ao produto</button>' +
      '</div></div></div></div></div></div>';
    return template;
  }
  return {
    link: function($scope, ele, attrs) {
      $scope.$watch($scope.gallery, function() {
        ele.html(buildTemplate($scope, ""));
        $compile(ele.contents())($scope);
      });
      $timeout(function() {
        console.log(ele[0]);
        console.log(ele[0].parentNode);
        window.ele = ele;
        var varId = ele[0].parentNode.id.split('-')[1];
        $scope.getVariantImages(varId);
        $scope.$watch($scope.variantImages[varId], function() {
          $timeout(function() {
            ele.html(buildTemplate($scope, varId));
            $compile(ele.contents())($scope);
          });
        });
      }, 1000);
    }
  };
});
