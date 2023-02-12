from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        work_order_id = self.env["fleet.work.order"].create({'repair_id': self.repair_id.id, })
        self.work_order_id = work_order_id.id
        self.repair_id.state = "approved"
        return res

    repair_id = fields.Many2one(comodel_name="fleet.repair")
    repair_count = fields.Integer(compute="_compute_repair_count")
    work_order_id = fields.Many2one(comodel_name="fleet.work.order")
    work_order_count = fields.Integer(compute="_compute_work_order_count")

    @api.depends("work_order_id")
    def _compute_work_order_count(self):
        for record in self:
            record.work_order_count = record.work_order_id and 1

    @api.depends("repair_id")
    def _compute_repair_count(self):
        for record in self:
            record.repair_count = record.repair_id and 1

    def action_view_repair(self):
        return {
            'name': _("Fleet Repair"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "fleet.repair",
            'domain': [('id', 'in', [self.repair_id.id])],
            'target': 'current',
        }

    def action_view_work_order(self):
        return {
            'name': _("Fleet Work Order"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "fleet.work.order",
            'domain': [('id', 'in', [self.work_order_id.id])],
            'target': 'current',
        }
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fleet_model_id = fields.Many2one(comodel_name="fleet.vehicle.model",
                                     string="Model #")
    license_plate = fields.Char()