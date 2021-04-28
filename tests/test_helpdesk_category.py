from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestHelpdeskCategory(TransactionCase):
    def setUp(self):
        super(TestHelpdeskCategory, self).setUp()
        usersobj = self.env['res.users'].search([('id', '=', 1)])
        self.user = usersobj.id if usersobj else self.env['res.users'].create({'name': 'TestBot', 'login': 'testbot@gmail.com'})
    
    def test_create_helpdesk_category(self):
        prefs = self.env['helpdeskcategory.model'].search([])
        if len(prefs) < 1: 
            self.category_id = self.env['helpdeskcategory.model'].create({
                    'name': 'Skills', 'user_ids': [(6, 0, [self.user])],'code': 1, 'email': 'test@gmail.com',
                    'auto_msgs': 'Thank you for submitting your ticket',
                })

            self.assertEqual(category_id.id, self.category_id.id)
