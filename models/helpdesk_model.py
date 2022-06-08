from odoo import _, api, exceptions, fields, models, tools
from odoo.tools import pycompat, ustr, formataddr
from odoo.tools.misc import clean_context
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta
from odoo.tools.safe_eval import safe_eval
import logging
import uuid

_logger = logging.getLogger(__name__)

TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'Medium priority'),
    ('3', 'High priority'),
    ('4', 'Urgent'),
]

class TicketModel(models.Model):
    _name = 'helpdeskticket.model'
    _description = "Helpdesk Ticket - Maach Media"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        # self = self.with_context(default_user_id=False)
        val = msg.get('from').split('<')[0]
        defaults = {
            'description': msg.get('subject') or _("No Subject"),
            'client_name': val,
            'client_email': msg.get('from'),
            'ticket_type': "issue",
            'note': msg.get("body"),
            'active': True,
            'category': self.env.ref('helpdesk_api.email_category').id,
            'priority': '2',
        }
        # if msg.get('priority'):
        #     defaults['priority'] = msg.get('priority')
        if custom_values:
            defaults.update(custom_values)
        return super(TicketModel, self).message_new(msg, custom_values=defaults)


    def _get_user_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('create_uid', '=', self.env.user.id)])
        if tickets:
            return int(tickets) if tickets else 0

    def _get_customer_centered_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('ticket_type', '=', 'customer')])
        return tickets if tickets else 0

    def _get_issue_other_centered_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('ticket_type', '=',['other', 'issue'])])
        return tickets if tickets else 0

    def _get_closed_tickets(self):
        closed_stage_id = self.env.ref('helpdesk_api.closed_stage_id').id
        tickets = self.env['helpdeskticket.model'].search_count([('create_uid', '=', self.env.user.id),('close_ticket', '=', True)])
        return tickets if tickets else 0

    def _get_opened_tickets(self):
        new_stage_id = self.env.ref('helpdesk_api.new_stage_id').id
        tickets = self.env['helpdeskticket.model'].search_count([('create_uid', '=', self.env.user.id),('close_ticket', '=', False)])
        return tickets if tickets else 0

    def _get_my_tickets_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('assigned_user', '=', self.env.user.id)])
        return tickets if tickets else 0

    def _get_solved_tickets(self):
        solved_stage_id = self.env.ref('helpdesk_api.solved_stage_id').id
        tickets = self.env['helpdeskticket.model'].search_count([('create_uid', '=', self.env.user.id),('close_ticket', '=', True), ('sla_failed', '=', False)])
        return tickets if tickets else 0

    def _get_unassigned_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('assigned_user', '=',False)])
        return tickets if tickets else 0

    def _get_failed_sla_tickets(self):
        progress_stage_id = self.env.ref('helpdesk_api.progress_stage_id').id
        new_stage_id = self.env.ref('helpdesk_api.new_stage_id').id
        tickets = self.env['helpdeskticket.model'].search_count([('create_uid', '=', self.env.user.id),('close_ticket', '=', False), ('sla_failed', '=', True)])

        # tickets = self.env['helpdeskticket.model'].search_count([('expected_date', '<', fields.Datetime.now()), ('stage_id', 'in', [False, progress_stage_id, new_stage_id])])
        return tickets if tickets else 0

    def _get_high_priority_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('priority', '=',3)])
        return tickets if tickets else 0

    def _get_urgent_priority_tickets(self):
        tickets = self.env['helpdeskticket.model'].search_count([('priority', '=', 4)])
        return tickets if tickets else 0

    # def create_action(self):
    # 	title = "Tickets"
    # 	action = self.env["ir.actions.actions"]._for_xml_id('helpdesk_api.helpdesk_my_ticket_action')
    # 	action['display_name'] = title
    # 	# action['search_view_id'] = self.env.ref(search_view_ref).read()[0]
    # 	action['views'] = [(False, view) for view in action['view_mode'].split(",")]
        
    # 	return {'action': action}

    @api.model
    def create_action(self, action_ref, title, search_view_ref):
        action = self.env["ir.actions.actions"]._for_xml_id(action_ref)
        if title:
            action['display_name'] = title
        if search_view_ref:
            action['search_view_id'] = self.env.ref(search_view_ref).read()[0]
        action['views'] = [(False, view) for view in action['view_mode'].split(",")]
        return {'action': action}
        
    # def create_action(self, domain="one"):
    # 	domain = [('create_uid', '=', self.env.user.id)]
    # 	title = "My tickets"
    # 	if domain == "two":
    # 		domain = [('create_uid', '=', self.env.user.id)]
        
    # 	tickets = self.env['helpdeskticket.model'].search(domain)
    # 	form_view_ref = self.env.ref('helpdesk_api.helpdeskticket_view_form')
    # 	search_view_ref = self.env.ref('helpdesk_api.helpdeskticket_model_view_search')
    # 	tree_view_ref = self.env.ref('helpdesk_api.helpdesktickets_view_tree')
        
    # 	return {
    # 		'domain': [('id', 'in', [rec.id for rec in tickets])],
    # 		'name': title,
    # 		'res_model': 'helpdeskticket.model',
    # 		'type': 'ir.actions.act_window',
    # 		'view_type': 'tree',
    # 		'views': [(tree_view_ref.id, 'tree')],
    # 		'search_view_id': search_view_ref and search_view_ref.id,
    # 	}

    def _domain_get_user_companies(self):
        domain = [('id', 'in', self.env.user.company_ids.ids)]
        return domain

    def _domain_company_categories(self):
        category = self.env['helpdeskcategory.model'].search([('company_id', 'in', self.env.user.company_ids.ids)])
        domain = [('id', 'in', category.ids)]
        return domain

    @api.model
    def get_dashboard_details(self):
        return {
            'create_user_ticket': self._get_user_tickets(),
            '_get_customer_centered_tickets': self._get_customer_centered_tickets(),
            '_get_issue_other_centered_tickets': self._get_issue_other_centered_tickets(),
            '_get_closed_tickets': self._get_closed_tickets(),
            '_get_opened_tickets': self._get_opened_tickets(),
            '_get_my_tickets_tickets': self._get_my_tickets_tickets(),
            '_get_solved_tickets': self._get_solved_tickets(),
            '_get_unassigned_tickets': self._get_unassigned_tickets(),
            '_get_failed_sla_tickets': self._get_failed_sla_tickets(),
            '_get_high_priority_tickets': self._get_high_priority_tickets(),
            '_get_urgent_priority_tickets': self._get_urgent_priority_tickets(),
        }

    name = fields.Char(string="Ticket Id")
    sla_failed = fields.Boolean(string="SLA Failed", default=False, store=True, compute="compute_sla_failed")
    description = fields.Char(string="Description")
    note = fields.Html(string="Notes")
    comment = fields.Html(string="Internal Note")
    assigned_user = fields.Many2one('res.users', string="Assigned To?")
    client_email = fields.Char(string="Client Email", store=True)
    client_name = fields.Char(string="Client Name")
    company_id = fields.Many2one('res.company', string="Company", domain=lambda self: self._domain_get_user_companies())
    partner_id = fields.Many2one("res.partner", string="Customer", required=False, default = lambda rec: rec.env.user.partner_id.id)
    email_logs = fields.Many2many("mail.mail", string="Mails", readonly=True)
    category = fields.Many2one("helpdeskcategory.model", string="Category", required=False,domain=lambda self: self._domain_company_categories())
    sla_id = fields.Many2one('helpdesk.tracker.sla', string="SLA", store=True)
    duration = fields.Integer(string="Duration")# , compute="compute_ticket_duration")
    num_tickets = fields.Integer(string="Tickets", default= lambda self: self._get_user_tickets())
    color = fields.Integer('Color')
    file = fields.Binary('Upload Document')
    file_name = fields.Char('File name')
    sla_duration = fields.Char('SLA Duration')
    diff_failed_sla_duration = fields.Integer('SLA Escalated(Days)')

    ticket_type = fields.Selection([('customer', 'Customer Centered'), ('issue', 'Issue'), ('other', 'Others')], default='customer', string="Ticket Type")
    priority = fields.Selection(
        TICKET_PRIORITY, string='Priority',
        help='Tickets under this priority will not be taken into account.')
    status = fields.Selection([('new', 'New'), ('open', 'Open'), ('close', 'Closed')], default='new', string="Status")
    submitted_date = fields.Datetime(string='Submitted Date')
    expected_date = fields.Datetime(string='Deadline Date', compute="compute_deadline_date", store=True, help="Compute SLA Fail to true if the current date is greater than the deadline date")
    write_ids = fields.Many2many('res.users', string="Modifiers", compute="compute_modifiers")
    stage_id = fields.Many2one('helpdeskstages.model', string="Stages", default=lambda s: s.env.ref('helpdesk_api.new_stage_id').id)
    active = fields.Boolean(string="Active", default=True)
    close_ticket = fields.Boolean(string="Closed", default=False)
    response = fields.Integer('Response time(hours)', default=1, required=False, compute="compute_sla_id")
    time_days = fields.Integer('Day(s)', default=0, help="Days to reach given stage based on ticket creation date", compute="compute_sla_id", store=True)
    time_hours = fields.Integer('Hour(s)', default=0, help="Hours to reach given stage based on ticket creation date", compute="compute_sla_id", store=True)

    @api.model
    def create(self, vals):
        record = super(TicketModel, self).create(vals)
        sequence = self.env['ir.sequence'].next_by_code('helpdeskticket.model')
        last_create_ticket = self.env['helpdeskticket.model'].search([])
        ticketid= f'TI00000 {str(last_create_ticket[-1].id)}' if last_create_ticket else f'TIC00000{self.id}'
        record.name = sequence or uuid.uuid1()
        return record
        
    def write(self, vals):
        if 'comment' in vals:
            body = '''Dear {0}, <br/>A comment was added on the ticket with ID {1} by {2}
            '''.format(self.partner_id.name or self.client_name, self.name, self.env.user.name)
            mail_id = self.send_mail(self.company_id.email, self.client_email, body, False)
        res = super(TicketModel, self).write(vals)
        vals['write_ids']= [(4, self.env.user.id)]
        return res

    def action_submit(self):
        self.status = 'open'
        self.submitted_date = fields.Datetime.now()
        self.send_stage_notification()
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            if rec.partner_id and rec.ticket_type != "issue":
                rec.client_email = rec.partner_id.email 
                rec.client_name = rec.partner_id.name 

    @api.onchange('priority')
    def onchange_priority(self):
        for rec in self:
            if rec.priority:
                sla = self.env['helpdesk.tracker.sla'].search([
                    # ('company_id', '=', self.company_id.id),
                    ('category_id', '=', self.category.id),
                    ('priority', '=', self.priority),
                    ], limit=1)
                if sla:
                    rec.sla_id = sla.id
                # else:
                # 	raise ValidationError('There is no sla generated for this priority')
 
    @api.depends('sla_id')
    def compute_sla_id(self):
        for rec in self:
            if rec.sla_id:
                rec.response = rec.sla_id.response 
                rec.time_days = rec.sla_id.time_days 
                rec.time_hours = rec.sla_id.time_hours 
            else:
                rec.response = False
                rec.time_days = False 
                rec.time_hours = False

    @api.depends('submitted_date', 'time_days', 'time_hours')
    def compute_deadline_date(self):
        for rec in self:
            submitted_date = rec.submitted_date
            if submitted_date:
                days = rec.time_days if rec.time_days > 0 else rec.category.highest_duration
                deadline_date = submitted_date + timedelta(days=days, hours=rec.time_hours, minutes=0)
                rec.expected_date = deadline_date
            else:
                rec.expected_date = False

    @api.depends('expected_date')
    def compute_sla_failed(self):
        for rec in self:
            if rec.expected_date:
                date_diff = fields.Datetime.now() - rec.expected_date
                if rec.expected_date < fields.Datetime.now() and self.close_ticket == False:
                    rec.sla_failed = True
                    rec.diff_failed_sla_duration = date_diff.days if date_diff.days > 0 else 0

                else:
                    rec.sla_failed = False 

    @api.depends('category')
    def compute_modifiers(self):
        for rec in self:
            if rec.category:
                rec.write_ids = [(4, usr.id) for usr in rec.category.mapped('user_ids')]
            else:
                rec.write_ids = False 

    @api.onchange('ticket_type')
    def compute_ticket_type(self):
        for rec in self:
            if rec.ticket_type and rec.ticket_type in ["issue"]:
                rec.client_email = False
                rec.client_name = False
                rec.partner_id = False
                rec.category = False
                rec.company_id = False

    @api.onchange('assigned_user')
    def onchange_assigned_user(self):
        for rec in self:
            if rec.assigned_user:
                body = "Dear {0}, <br/>This is to inform you that ticket with ID {1}\
                        have been assigned to - {2}.<br/>\
                        Regards".format(rec.partner_id.name or rec.client_name, rec.name, rec.assigned_user.name)
                mail_id = rec.send_mail(rec.company_id.email, rec.client_email, body, False) 
                rec.write({'email_logs': [(4, mail_id.id)]})

    @api.onchange('category')
    def _get_stages(self):
        for rec in self:
            if rec.category:
                lists = []
                stage_ids = self.env['helpdeskstages.model'].search([])
                sla_ids = self.env['helpdesk.tracker.sla'].search([('category_id', '=', rec.category.id)])
                for stg in stage_ids:
                    categ_ids = stg.mapped('apply_on').filtered(lambda s: s.id == self.category.id)
                    if categ_ids:
                        lists.append(stg.id)
                domain = {'stage_id': [('id', 'in', lists)], 'sla_id': [('id', 'in', [sla.id for sla in sla_ids])]}
                return {'domain': domain}
    
    @api.onchange('stage_id')
    def move_stage_action(self):
        if self.description:
            user = self.env['res.users'].browse([self.env.uid])
            helpdesk_manager = user.has_group("helpdesk_api.group_helpdesk_issue_manager")
            if not helpdesk_manager:
                raise ValidationError("Sorry !!! You are not allowed to modify the status of this ticket")
            closed_stage_id = self.env.ref('helpdesk_api.closed_stage_id').id
            solved_stage_id = self.env.ref('helpdesk_api.solved_stage_id').id
            if self.stage_id.id in [solved_stage_id, closed_stage_id]:
                self.close_ticket = True
            self.send_stage_notification()

    @api.onchange('close_ticket')
    def _onchange_close_ticket_checkbox(self):
        new_stage_id = self.env.ref('helpdesk_api.new_stage_id').id
        if self.stage_id.id != new_stage_id:
            if self.close_ticket == True:
                self.status = 'open'
            else:
                self.status = 'close'

    def toggle_close_ticket_action(self):
        for rec in self: 
            progress_stage_id = self.env.ref('helpdesk_api.progress_stage_id').id
            closed_stage_id = self.env.ref('helpdesk_api.closed_stage_id').id
            if rec.close_ticket:
                rec.stage_id = progress_stage_id
                rec.close_ticket = False
            else:
                rec.stage_id = closed_stage_id
                rec.close_ticket = True
            body = "Dear {0}, <br/>This is to inform you that ticket with ID {1}\
                 have been {2}. Kindly Confirm by replying to this mail.<br/>\
                 Regards".format(rec.partner_id.name or rec.client_name, rec.name, rec.stage_id.name)
            mail_id = rec.send_mail(self.company_id.email, self.client_email, body, False)
            rec.write({
                'email_logs': [(4, mail_id.id)]
            })

    def assign_issue(self):
        for rec in self:
            progress_stage_id = self.env.ref('helpdesk_api.progress_stage_id').id
            rec.assigned_user = self.env.user.id
            body = "Dear {0}, <br/>This is to inform you that ticket with ID {1}\
                 is in progress and have been assigned to - {2}.<br/>\
                 Regards".format(rec.partner_id.name or rec.client_name, rec.name, rec.assigned_user.name)
            mail_id = self.send_mail(self.company_id.email, self.client_email, body, False) 
            rec.write({
            'email_logs': [(4, mail_id.id)], 'status': 'open', 'stage_id': progress_stage_id,
            })

    def send_stage_notification(self):
        for rec in self: 
            user = self.env.user.name
            body = f"Dear {rec.partner_id.name or rec.client_name}, <br/>This is to inform you that ticket with ID {rec.name}\
                 is moved to {rec.stage_id.name or 'progress'} by {user}.<br/>\
                 Regards"
            mail_id = self.send_mail(self.company_id.email, self.client_email, body, False) 
            rec.update({
            'email_logs': [(4, mail_id.id)]
            })

    def all_my_tickets(self):
        return self.get_my_ticket_action_record()

    def toggle_active(self):
        self.active = True if self.active == False else False  

    def validate_and_get_email(self):
        email_to = None
        if self.client_email:
            email_to = self.client_email

        if self.partner_id and not self.partner_id.email:
            raise ValidationError('The selected partner does not have an email configured')
        else:
            email_to = self.partner_id.email
        return email_to

    def send_by_mail_button(self):
        if not self.category:
            raise ValidationError("Please select a category")
        body = f"Hi {self.partner_id.name or self.client_name}, your ticket with ID {self.name} is currently been handled. The status is: {self.stage_id.name} \n Thanks"
        mail_id = self.send_mail(self.env.user.email, self.client_email, body, False)
        self.write({
            'email_logs': [(4, mail_id.id)]
        })

    def send_mail(self, email_from, mail_to, body, attachment=None):
        # email_template = self.env.ref('helpdesk_api.send_helpdesk_email_template')
        # """args: inform_internal_users determines if the mail is sent to users who picks up the ticket"""
        # body = email_template.body_html
        #  if inform_internal_users else custom_body if custom_body else "Ticket have been generated with ID # {}".format(self.name)
        subject_msg = self.name # if not client_send else self.category.auto_msgs() 
        subject = "HELPDESK NOTIFICATION #{}".format(subject_msg)
        recipients = [rec.login for rec in self.category.mapped('user_ids')]
        mail_data = {
            'email_from': email_from,
            'subject': subject,
            'email_to': mail_to,
            'email_cc': ','.join(recipients) if False not in recipients else False,
            'body_html': body,
        }
        mail_id = self.env['mail.mail'].create(mail_data)
        return mail_id 
        
        # self.env['mail.mail'].send(mail_id)
 
    def get_record_reference(self):
        reference_id = self.env['helpdeskticket.model'].search([('id', '=', self.id)])
        if not reference_id:
            raise ValidationError('There is no related record found!.')
        resp = {
            'type': 'ir.actions.act_window',
            'name': _('Reference'),
            'res_model': 'helpdeskticket.model',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': reference_id.id
        }
        return resp

    def _get_action(self, action_form_xmlid, action_tree_xmlid):
        tree_view_ref = self.env.ref(action_tree_xmlid, False)
        form_view_ref = self.env.ref(action_form_xmlid, False)
        domain = None
        helpdesk_all = self.env['helpdeskticket.model'].search([('assigned_user', '=', self.env.user.id), ('write_ids', 'in', [self.assigned_user.id])])
        return {
            'domain': [('id', 'in', [rec.id for rec in helpdesk_all])],
            'name': 'My Tickets',
            'res_model': 'helpdeskticket.model',
            'type': 'ir.actions.act_window',
            'views': [(tree_view_ref.id, 'tree'),(form_view_ref.id, 'form')],
        } 

    # @api.multi
    def get_my_ticket_action_record(self):
        return self._get_action('helpdesk_api.helpdeskticket_view_form', 'helpdesk_api.helpdesktickets_view_tree')

