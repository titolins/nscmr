FROM grahamdumpleton/mod-wsgi-docker:python-3.4-onbuild

CMD [ "--url-alias", "/static", "nscmr/static", \
      "--url-alias", "/admin/static", "nscmr/admin/static", \
      "--url-alias", "/_uploads/productImages/", \
        "instance/uploads/img/product/", \
      "--url-alias", "/_uploads/categoryImages/", \
        "instance/uploads/img/category/", \
      "--server-name", "http://www.studioduvet.com.br", \
      "nscmr.wsgi" ]

