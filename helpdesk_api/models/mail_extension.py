from odoo import models, fields, api 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
 

class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, vals):
        HelpdeskTicket = self.env['helpdeskticket.model']
        if 'email_to' and 'email_from' in vals:
            if 'support@qisolutions.co.za' in vals.get('email_to') or vals.get('email_to') in ['support@qisolutions.co.za'] or vals.get('email_to').startswith('support@qis'):
                email_from = vals.get("email_from").split('<')
                c_email = email_from
                if len(email_from) > 0:
                    c_email = email_from[1].replace('>', "")
                val = {
                    'description': vals.get("subject"),
                    'client_email': c_email, # email_from[1].replace('>', "") if len(email_from) > 0 else email_from,
                    'client_name': vals.get("email_from").split('<')[0].replace('"', "") if email_from else "",
                    'note': vals.get("body_html"),
                    'ticket_type': "issue",
                    'active': True,
                    'category': self.env.ref('helpdesk_api.email_category').id,
                    'priority': '2',
                    }
                ticket = HelpdeskTicket.sudo().create(val)
                ticket.action_submit()
                # ticket.onchange_sla_id()
                # ticket.compute_ticket_deadline()

        return super(MailMail, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     HelpdeskTicket = self.env['helpdeskticket.model']
    #     if 'email_to' and 'email_from' in vals:
    #         if vals.get('email_to') or vals.get('email_to') == 'support@qisolutions.co.za':
    #             email_from = vals.get("email_from").split('<')
    #             c_email = email_from
    #             if len(email_from) > 0:
    #                 raise ValidationError(vals.get('email_to'))
    #                 c_email = email_from[1].replace('>', "")
    #             val = {
    #                 'description': vals.get("subject"),
    #                 'client_email': c_email, # email_from[1].replace('>', "") if len(email_from) > 0 else email_from,
    #                 'client_name': vals.get("email_from").split('<')[0].replace('"', "") if email_from else "",
    #                 'note': vals.get("body_html"),
    #                 'ticket_type': "issue",
    #                 'active': True,
    #                 'category': self.env.ref('helpdesk_api.email_category').id,
    #                 'priority': '2',
    #                 }
    #             ticket = HelpdeskTicket.sudo().create(val)
    #             ticket.action_submit()
    #             # ticket.onchange_sla_id()
    #             # ticket.compute_ticket_deadline()
    #     return super(MailMail, self).create(vals)


    
