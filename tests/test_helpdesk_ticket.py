from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        usersobj = self.env['res.users'].search([('id', '=', 1)])
        self.user = usersobj if usersobj else self.env['res.users'].create({'name': 'TestBot', 'login': 'testbot@gmail.com'})

    def test_create_helpdesk_ticket(self):
        tickets = self.env['helpdeskticket.model'].search([])
        categorys = self.env['helpdeskcategory.model'].search([])
        stages = self.env['helpdeskstages.model'].search([])
        self.category_id = self.env['helpdeskcategory.model'].create({
                    'name': 'Stage 1', 'user_ids': [(6, 0, [self.user.id])],'sequence': 1, 'email': 'test@gmail.com',
                    'auto_msgs': 'Thank you for submitting your ticket',
                })

        self.stage_id = self.env['helpdeskstages.model'].create({
                    'name': 'Skills', 'apply_on': [(6, 0, [self.category_id.id])],'code': 1, 'is_close': False,
                })

        if len(tickets) < 1:
            self.ticket = self.env['helpdeskticket.model'].create({
                    'description': 'Request for skills', 'write_ids': [(6, 0, [self.user.id])],'priority': 'low', 'client_name': 'Maduka Sopulu',
                    'note': 'Issues to track via this ticket', 'assigned_user': self.user.id, 'client_email': "testclient@yahoo.com",
                    'expected_date': datetime.strptime("12/10/2010", "%m/%d/%Y"), 'category': self.category_id.id, 
                    'stage_id': self.stage_id.id
                })

            self.assertEqual(ticket.id, category_id.id)
