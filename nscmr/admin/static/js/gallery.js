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
.controller("GalleryController", ["$scope","$http", function($scope, $http) {
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
      $scope.$apply(function() {
        $scope.gallery = response.data;
      });
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
      $scope.getVariantImages(variantId);
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
      $scope.getVariantImages(variantId);
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
    $http({
      url: addImagesUri + '/' + varId,
      headers: {
        "Accept": "application/json;utf-8"
      }
    }).then(function success(response) {
      $scope.$apply(function() {
        $scope.variantImages[varId] = response.data;
      });
    }, function error(response) {
      console.log(response);
    });
  };

  $scope.updateGallery();
}]).directive('gallery', function($compile, $timeout) {
  function buildTemplate($scope) {
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
    template += '<a ng-repeat="p in variantImages[varId]" href="#" ng-click="selectVariantImage($event)">' +
      '<div class="col-xs-4 img-selector" id="{a p[\'id\'] a}">' +
      '<img src="{a p[\'thumb\'] a}" class="img-responsive"></img></div></a>';
    template += '<div class="clearfix"></div>';
    template += '<button ng-click="removeImages($event)" type="button" class="btn btn-primary">Remover fotos do produto</button></div>' +
    '<div id="img-gallery-pane" role="tabpanel" class="tab-pane img-gallery">';
    template += '' +
    '<a ng-repeat="p in gallery" href="#" ng-click="selectImage($event)">' +
      '<div class="col-xs-4 img-selector" id="{a p[\'id\'] a}">' +
        '<img class="img-responsive" src="{a p[\'thumb\'] a}"></img>' +
      '</div>' +
    '</a>';
    template += '' +
      '<div class="clearfix"></div>' +
      '<button ng-click="addImages($event)" type="button" class="btn btn-primary">Adicionar foto ao produto</button>' +
      '</div></div></div></div></div></div>';
    return template;
  }
  return {
    controller: "GalleryController",
    scope: {
      varId: '@',
    },
    link: function($scope, ele, attrs) {
      $scope.variantImages[$scope.varId] = [];
      $scope.getVariantImages($scope.varId);
      ele.html(buildTemplate($scope));
      $compile(ele.contents())($scope);
    }
  };
});
