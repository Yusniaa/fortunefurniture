# -*- coding: utf-8 -*-
# from odoo import http


# class Fortunefurniture(http.Controller):
#     @http.route('/fortunefurniture/fortunefurniture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fortunefurniture/fortunefurniture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fortunefurniture.listing', {
#             'root': '/fortunefurniture/fortunefurniture',
#             'objects': http.request.env['fortunefurniture.fortunefurniture'].search([]),
#         })

#     @http.route('/fortunefurniture/fortunefurniture/objects/<model("fortunefurniture.fortunefurniture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fortunefurniture.object', {
#             'object': obj
#         })
