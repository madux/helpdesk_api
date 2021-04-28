from odoo import models, fields, api 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
 

class TicketCategory(models.Model):
    _name = 'helpdeskcategory.model'

    name = fields.Char(string="Description")
    user_ids = fields.Many2many('res.users', string="Users", required=True)
    code = fields.Integer('Code', size=100, readonly=True)
    email = fields.Char('Email', required=False)
    active = fields.Boolean(string="Active", default=True)
    auto_msgs = fields.Text('Automated answer', size=200, help="Default message to send as mail when ticket is created from External Sources")
    highest_duration = fields.Integer('Highest Duration of Ticket(Days)', default=1)
    custom_html = fields.Text('Custom Message', required=True, size=100, help="Default message to send as mail when ticket moves from stages to another")

    @api.model
    def create(self, vals):
        """Adds 1 to field code when it gets the last record"""
        last_rec = self.search([])
        new_code = last_rec[-1].code + 1 if last_rec else 1
        vals['code'] = new_code
        return super(TicketCategory, self).create(vals)

    def automated_answer(self):
        return self.auto_msgs if self.auto_msgs else "Your request have been submitted"
