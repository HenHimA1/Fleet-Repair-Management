from odoo import models, fields, api, _


class FleetRepair(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'fleet.work.order'
    _description = 'Fleet Work Order'

    name = fields.Char(string="Name",
                       related='subject')
    repair_id = fields.Many2one(comodel_name="fleet.repair")
    repair_line_ids = fields.One2many(comodel_name="fleet.repair.line",
                                      related='repair_id.line_ids')
    repair_count = fields.Integer(compute="_compute_repair_count")
    sale_ids = fields.One2many("sale.order", related='repair_id.sale_ids')
    sale_count = fields.Integer(related='repair_id.sale_count')
    diagnosis_ids = fields.One2many("fleet.diagnosis",
                                    related='repair_id.diagnosis_ids')
    diagnosis_count = fields.Integer(related='repair_id.diagnosis_count')
    subject = fields.Char(string="Work Order",
                          related='repair_id.subject')
    scheduled_start_date = fields.Datetime()
    scheduled_end_date = fields.Datetime()
    actual_start_date = fields.Datetime()
    actual_end_date = fields.Datetime()
    date = fields.Date(string="Date")
    partner_id = fields.Many2one(comodel_name="res.partner",
                                 related='repair_id.partner_id',
                                 string="Client")
    priority = fields.Selection(related='repair_id.priority',)
    state = fields.Selection(selection=[('cancel', 'Cancel'),
                                        ('draft', 'Draft'),
                                        ('pending', 'Pending'),
                                        ('progress', 'In Progress'),
                                        ('finished', 'Finished'),],
                             string='Status',
                             required=True,
                             readonly=True,
                             copy=False,
                             tracking=True,
                             default='draft',)
    phone = fields.Char(string='Phone',
                        related='repair_id.phone')
    user_id = fields.Many2one(comodel_name="res.users",
                              related='repair_id.user_id',
                              string="Assigned to")
    technician_id = fields.Many2one(comodel_name="res.users",
                                    related='repair_id.technician_id',
                                    string="Technician")
    number_hour = fields.Float(string="Number of Hours")
    duration = fields.Float(string="Duration")
    work_hour = fields.Float(string="Hours Worked")

    def action_start(self):
        for record in self:
            record.actual_start_date = fields.datetime.now()
            record.state = "progress"
            record.repair_id.state = "progress"

    def action_pending(self):
        for record in self:
            record.state = "pending"

    def action_resume(self):
        for record in self:
            record.state = "progress"

    def action_finished(self):
        for record in self:
            record.actual_end_date = fields.datetime.now()
            record.state = "finished"
            record.repair_id.state = "done"

    def action_cancel(self):
        for record in self:
            record.state = "cancel"

    def action_view_diagnosis(self):
        return {
            'name': _("Fleet Diagnosis"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': "fleet.diagnosis",
            'domain': [('id', 'in', self.diagnosis_ids.ids)],
            'target': 'current',
        }

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

    @api.depends("repair_id")
    def _compute_repair_count(self):
        for record in self:
            record.repair_count = record.repair_id.id and 1
