# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

FUEL_TYPES = [
    ('diesel', 'Diesel'),
    ('gasoline', 'Gasoline'),
    ('full_hybrid', 'Full Hybrid'),
    ('plug_in_hybrid_diesel', 'Plug-in Hybrid Diesel'),
    ('plug_in_hybrid_gasoline', 'Plug-in Hybrid Gasoline'),
    ('cng', 'CNG'),
    ('lpg', 'LPG'),
    ('hydrogen', 'Hydrogen'),
    ('electric', 'Electric'),
]


class FleetRepair(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'fleet.repair'
    _description = 'Fleet Repair'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["name"] = self.env['ir.sequence'].next_by_code('fleet.repair')
        return super(FleetRepair, self).create(vals_list)

    name = fields.Char(default="New")
    subject = fields.Char(required=True)
    state = fields.Selection(selection=[('received', 'Received'),
                                        ('diagnosis', 'In Diagnosis'),
                                        ('sent', 'Quotation Sent'),
                                        ('approved', 'Quotation Approved'),
                                        ('progress', 'Work in Progress'),
                                        ('done', 'Done'),],
                             string='Status',
                             required=True,
                             readonly=True,
                             copy=False,
                             tracking=True,
                             default='received',)
    receipt_date = fields.Date(string="Date of Receipt")
    priority = fields.Selection(selection=[('0', 'Low'),
                                           ('1', 'Normal'),
                                           ('2', 'High'),])
    user_id = fields.Many2one(comodel_name="res.users",
                              required=True,
                              string="Assigned to")
    technician_id = fields.Many2one(comodel_name="res.users",
                                    string="Technician")
    partner_id = fields.Many2one(comodel_name="res.partner",
                                 required=True,
                                 string="Client")
    line_ids = fields.One2many(comodel_name="fleet.repair.line",
                               inverse_name="repair_id")
    contact_name = fields.Char()
    contact_number = fields.Char()
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    notes = fields.Text()
    sale_ids = fields.One2many(comodel_name="sale.order",
                               inverse_name="repair_id")
    sale_count = fields.Integer(compute="_compute_sale_count")
    diagnosis_ids = fields.One2many(comodel_name="fleet.diagnosis",
                                    inverse_name="repair_id")
    diagnosis_count = fields.Integer(compute="_compute_diagnosis_count")
    work_order_ids = fields.One2many(comodel_name="fleet.work.order",
                                     inverse_name="repair_id")
    work_order_count = fields.Integer(compute="_compute_work_order_count")

    def action_create_fleet_diagnosis(self):
        for record in self:
            record.diagnosis_ids = [(0, 0, {"repair_id": record.id,
                                            "repair_line_ids": [(4, line_id.id) for line_id in record.line_ids]})]
            for line_id in record.line_ids:
                line_id.state = "diagnosis"
            record.state = "diagnosis"

            return {'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': "fleet.diagnosis",
                    'res_id': record.diagnosis_ids.ids[0],
                    'target': 'current', }

    @api.depends("work_order_ids")
    def _compute_work_order_count(self):
        for record in self:
            record.work_order_count = len(record.work_order_ids.ids)

    @api.depends("sale_ids")
    def _compute_sale_count(self):
        for record in self:
            record.sale_count = len(record.sale_ids.ids)

    @api.depends("diagnosis_ids")
    def _compute_diagnosis_count(self):
        for record in self:
            record.diagnosis_count = len(record.diagnosis_ids.ids)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        for record in self:
            record.email = record.partner_id.email
            record.phone = record.partner_id.phone
            record.mobile = record.partner_id.mobile

    def action_view_diagnosis(self):
        return {
            'name': _("Fleet Diagnosis"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "fleet.diagnosis",
            'domain': [('id', 'in', self.diagnosis_ids.ids)],
            'target': 'current',
        }

    def action_view_sale(self):
        return {
            'name': _("Sale Order"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "sale.order",
            'domain': [('id', 'in', self.sale_ids.ids)],
            'target': 'current',
        }

    def action_view_work_order(self):
        return {
            'name': _("Fleet Work Order"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "fleet.work.order",
            'domain': [('id', 'in', self.work_order_ids.ids)],
            'target': 'current',
        }


class FleetRepairLine(models.Model):
    _name = 'fleet.repair.line'
    _description = 'Fleet Repair Line'

    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('diagnosis', 'In Diagnosis'),
                                        ('done', 'Done'),],
                             default="draft")
    repair_id = fields.Many2one(comodel_name="fleet.repair",
                                ondelete='cascade',)
    part_ids = fields.One2many(comodel_name="fleet.repair.part",
                               inverse_name="repair_line_id")
    diagnosis_id = fields.Many2one(comodel_name="fleet.diagnosis")
    service_id = fields.Many2one(comodel_name="fleet.vehicle.log.services",
                                 string="Nature of Service")
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle",
                                 string="Fleet")
    license_plate = fields.Char()
    model_id = fields.Many2one(comodel_name="fleet.vehicle.model")
    vin_sn = fields.Char(string="Chassis Number")
    fuel_type = fields.Selection(selection=FUEL_TYPES)
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('diagnosis', 'In Diagnosis'),
                                        ('done', 'Done'),],
                             string='Status',
                             required=True,
                             readonly=True,
                             copy=False,
                             default='draft',)
    is_guarantee = fields.Selection(selection=[('yes', 'Yes'),
                                               ('no', 'No')],
                                    string="Under Guarantee?")
    guarantee_type = fields.Selection(selection=[('paid', 'Paid'),
                                                 ('free', 'Free')])
    notes = fields.Text()
    results = fields.Text()

    @api.onchange("vehicle_id")
    def _onchange_vehicle_id(self):
        for record in self:
            record.license_plate = record.vehicle_id.license_plate
            record.model_id = record.vehicle_id.model_id.id
            record.vin_sn = record.vehicle_id.vin_sn

    def action_enter_result(self):
        for record in self:
            record.state = "done"


class FleetRepairPart(models.Model):
    _name = 'fleet.repair.part'
    _description = 'Fleet Diagnosis Part'

    repair_line_id = fields.Many2one(comodel_name="fleet.repair.line",
                                     ondelete="cascade")
    product_id = fields.Many2one(comodel_name="product.product",
                                 required=True)
    code = fields.Char()
    qty = fields.Float(required=True,
                       default=1)
    price_unit = fields.Float()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for record in self:
            record.code = record.product_id.code
            record.price_unit = record.product_id.lst_price
