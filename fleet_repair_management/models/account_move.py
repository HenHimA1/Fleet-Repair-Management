from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    repair_ids = fields.Many2many(comodel_name="fleet.repair",
                                 compute="_compute_repair_ids")
    repair_count = fields.Integer(compute="_compute_repair_count",
                                  store=True)

    @api.depends("line_ids")
    def _compute_repair_ids(self):
        for record in self:
            repair_ids = []
            for line_id in record.line_ids:
                for sale_line_id in line_id.sale_line_ids:
                    repair_ids.append(sale_line_id.order_id.repair_id.id)
            record.repair_ids = repair_ids

    @api.depends("repair_ids")
    def _compute_repair_count(self):
        for record in self:
            record.repair_count = len(record.repair_ids.ids)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fleet_model_id = fields.Many2one(comodel_name="fleet.vehicle.model",
                                     string="Model #",
                                     related='sale_line_id.fleet_model_id')
    license_plate = fields.Char(related='sale_line_id.license_plate')
    sale_line_id = fields.Many2one(comodel_name="sale.order.line",
                                   compute="_compute_sale_line_id")

    @api.depends("sale_line_ids")
    def _compute_sale_line_id(self):
        for record in self:
            record.sale_line_id = record.sale_line_ids.ids and record.sale_line_ids.ids[0]
