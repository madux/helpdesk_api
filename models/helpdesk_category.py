from odoo import models, fields, api 
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
 

TICKET_PRIORITY = [
	('0', 'All'),
	('1', 'Low priority'),
	('2', 'Medium priority'),
	('3', 'High priority'),
	('4', 'Urgent'),
]


class HelpdeskDeskTracker(models.Model):
	_name = 'helpdesk.tracker.sla'
	name = fields.Char('SLA Policy Name', required=True, index=True)
	description = fields.Text('SLA Policy Description')
	active = fields.Boolean('Active', default=True)
	category_id = fields.Many2one('helpdeskcategory.model', 'Category', required=True)
	stage_id = fields.Many2one(
		'helpdeskstages.model', 'Target Stage', required=True,
		help='Minimum stage a ticket needs to reach in order to satisfy this SLA.', ondelete="cascade")
	priority = fields.Selection(
		TICKET_PRIORITY, string='Minimum Priority',
		default='0', required=True,
		help='Tickets under this priority will not be taken into account.')
	company_id = fields.Many2one('res.company', 'Company', readonly=True, store=True)
	response = fields.Integer('Response time(hours)', default=1, required=False)
	time_days = fields.Integer('Days', default=0, required=True, help="Days to reach given stage based on ticket creation date")
	time_hours = fields.Integer('Hours', default=0, required=True, help="Hours to reach given stage based on ticket creation date")

	# @api.onchange('time_hours')
	# def _onchange_time_hours(self):
	# 	resource_calendar = self.env.company.resource_calendar_id
	# 	avg_hour = resource_calendar.hours_per_day
	# 	if self.time_hours >= avg_hour:
	# 		self.time_days += self.time_hours / avg_hour
	# 		self.time_hours = self.time_hours % avg_hour


class TicketCategory(models.Model):
	_name = 'helpdeskcategory.model'

	name = fields.Char(string="Description")
	user_ids = fields.Many2many('res.users', string="Users", required=True)
	code = fields.Integer('Code', size=100, readonly=True)
	email = fields.Char('Email', required=False)
	active = fields.Boolean(string="Active", default=True)
	auto_msgs = fields.Text('Automated answer', size=200, help="Default message to send as mail when ticket is created from External Sources")
	highest_duration = fields.Integer('Highest Duration of Ticket(Days)', default=1)
	custom_html = fields.Text('Custom Message', required=False, size=100, help="Default message to send as mail when ticket moves from stages to another")
	use_sla = fields.Boolean('SLA Policies')
	sla_id = fields.Many2one('helpdesk.tracker.sla', string="SLA")
	company_id = fields.Many2one('res.company', 'Company', store=True)

	@api.model
	def create(self, vals):
		"""Adds 1 to field code when it gets the last record"""
		last_rec = self.search([])
		new_code = last_rec[-1].code + 1 if last_rec else 1
		vals['code'] = new_code
		return super(TicketCategory, self).create(vals)

	def automated_answer(self):
		return self.auto_msgs if self.auto_msgs else "Your request have been submitted"
