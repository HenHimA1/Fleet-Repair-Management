# -*- coding: utf-8 -*-
# from odoo import http


# class Project/kerja/fleetRepairManagement(http.Controller):
#     @http.route('/project/kerja/fleet_repair_management/project/kerja/fleet_repair_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project/kerja/fleet_repair_management/project/kerja/fleet_repair_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project/kerja/fleet_repair_management.listing', {
#             'root': '/project/kerja/fleet_repair_management/project/kerja/fleet_repair_management',
#             'objects': http.request.env['project/kerja/fleet_repair_management.project/kerja/fleet_repair_management'].search([]),
#         })

#     @http.route('/project/kerja/fleet_repair_management/project/kerja/fleet_repair_management/objects/<model("project/kerja/fleet_repair_management.project/kerja/fleet_repair_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project/kerja/fleet_repair_management.object', {
#             'object': obj
#         })
