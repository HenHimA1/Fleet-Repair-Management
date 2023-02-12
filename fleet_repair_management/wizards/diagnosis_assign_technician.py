from odoo import models, fields


class DiagnosisAssignTechnician(models.TransientModel):
    _name = 'diagnosis.assign.technician'
    _description = "Diagnosis Assign Technician"

    diagnosis_id = fields.Many2one(comodel_name="fleet.diagnosis")
    technician_id = fields.Many2one(comodel_name="res.users",
                                    required=True,
                                    string="Technician")

    def action_confirm(self):
        for record in self:
            record.diagnosis_id.repair_id.sudo().write({"technician_id": record.technician_id.id})
            record.diagnosis_id.state = "progress"
