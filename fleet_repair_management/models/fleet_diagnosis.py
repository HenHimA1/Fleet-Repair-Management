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


class FleetDiagnosis(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'fleet.diagnosis'
    _description = 'Fleet Diagnosis'

    repair_id = fields.Many2one(comodel_name="fleet.repair",
                                ondelete="cascade")
    repair_line_ids = fields.One2many(comodel_name="fleet.repair.line",
                                      related='repair_id.line_ids')
    line_ids = fields.Many2many("fleet.repair.line",
                                compute="_compute_line_ids",
                                readonly=False)
    repair_count = fields.Integer(compute="_compute_repair_count")
    sale_ids = fields.One2many("sale.order",
                               related='repair_id.sale_ids')
    sale_count = fields.Integer(related='repair_id.sale_count')
    name = fields.Char(related='repair_id.name')
    subject = fields.Char(related='repair_id.subject')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('progress', 'In Progress'),
                                        ('complete', 'Complete'),],
                             string='Status',
                             required=True,
                             copy=False,
                             tracking=True,
                             default='draft',)
    receipt_date = fields.Date(related='repair_id.receipt_date',
                               string="Date of Receipt")
    priority = fields.Selection(related='repair_id.priority',)
    user_id = fields.Many2one(comodel_name="res.users",
                              related='repair_id.user_id',
                              string="Assigned to")
    technician_id = fields.Many2one(comodel_name="res.users",
                                    related='repair_id.technician_id',
                                    string="Technician")
    partner_id = fields.Many2one(comodel_name="res.partner",
                                 related='repair_id.partner_id')
    contact_name = fields.Char(related='repair_id.contact_name')
    contact_number = fields.Char(related='repair_id.contact_number')
    email = fields.Char(string='Email',
                        related='repair_id.email')
    phone = fields.Char(string='Phone',
                        related='repair_id.phone')
    mobile = fields.Char(string='Mobile',
                         related='repair_id.mobile')
    notes = fields.Text()

    def action_assign_to_technician(self):
        return {'name': _('Assign to Technician'),
                'res_model': 'diagnosis.assign.technician',
                'view_mode': 'form',
                'context': {'default_diagnosis_id': self.id},
                'target': 'new',
                'type': 'ir.actions.act_window', }

    def action_view_repair(self):
        return {
            'name': _("Fleet Repair"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "fleet.repair",
            'domain': [('id', 'in', [self.repair_id.id])],
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

    def action_create_quotation(self):
        for record in self:
            order_line = []
            for line_id in record.repair_line_ids:
                for part_id in line_id.part_ids:
                    order_line += [(0, 0, {"fleet_model_id": line_id.model_id.id,
                                           "license_plate": line_id.license_plate,
                                           "product_id": part_id.product_id.id,
                                           "product_uom_qty": part_id.qty,
                                           "price_unit": part_id.price_unit})]
            record.repair_id.sale_ids = [
                (0, 0, {"partner_id": record.partner_id.id,
                        "state": "draft",
                        "order_line": order_line})]
            record.repair_id.state = "sent"
            record.state = "complete"

            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': "sale.order",
                'res_id': self.sale_ids.ids[0],
                'target': 'current',
            }

    @api.depends("repair_id")
    def _compute_repair_count(self):
        for record in self:
            record.repair_count = record.repair_id.id and 1

    @api.depends("repair_line_ids")
    def _compute_line_ids(self):
        for record in self:
            record.line_ids = [(6, 0, record.repair_line_ids.ids)]
