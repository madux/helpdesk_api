from odoo import models, fields, api 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
 

class TicketStages(models.Model):
    _name = 'helpdeskstages.model'

    name = fields.Char(string="Description")
    sequence = fields.Integer('sequence', size=100, required=True)
    active = fields.Boolean(string="Active", default=True)
    apply_on = fields.Many2many('helpdeskcategory.model', string="Apply to", required=False)
    is_close = fields.Boolean(string="Is closed?",)

    # @api.multi
    # def write(self, vals):
    #     # raise ValidationError('You cannot use the same sequence used for other stages')
    #     seq_exist = self.env['helpdeskstages.model'].search([]).filtered(lambda s: s.sequence == vals.get('sequence'))
    #     if seq_exist:
    #         raise ValidationError('You cannot use the same sequence used for other stages')
    #     return super(TicketStages, self).write(vals)

    
