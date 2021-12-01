"""Part of odoo. See LICENSE file for full copyright and licensing details."""

import logging
from odoo import api, fields, models, _
import requests
from odoo import http 
from odoo.http import request
import json
from odoo.exceptions import ValidationError
from datetime import datetime
_logger = logging.getLogger(__name__)


class APIController(http.Controller):

    # data = {
    #     "contact_details": {
    #         'client_name': "Ebuka Chinedu", 
    #         'client_email': "Ebuka Chinedu", 
    #         'client_phone': "+2347067979346", 
    #         },
    #     "ticket_items": {
    #         "description": "Request for a fix...",
    #         "category_id": 1,
    #         "priority": 1', #1 high,  2 medium, 3 low
    #     }

    # }

    def validate_fields(self, data):
        error_item = []
        contact = data.get('contact_details')
        ticket_item = data.get('ticket_items')
        description = ticket_item.get('description')  
        category_id = ticket_item.get('category_id')
        if not contact:
            error_item.append("Contact Details must be provided\n ")
        else:
            client_email = contact.get('client_email', 0)
            client_name = contact.get('client_name', 0)
            if not client_email:
                error_item.append("Customer Email must be provided\n ")
            if not client_name:
                error_item.append("Customer Name must be provided\n ")
        if not category_id:
            error_item.append("Ticket Category must be provided\n ") 

        else:
            if type(category_id) not in [int]:
                error_item.append("Category Value must be an integer\n ")
            category_ref = request.env['helpdeskcategory.model'].sudo().search([('id', '=', int(category_id))], limit=1)
            if not category_ref:
                error_item.append("Category ID provide is not existing on the database \n ") 
        return error_item


    @http.route("/api/v1/issue/create", type="json", auth="public", methods=["POST", "GET"], csrf=False)
    def helpdesk_issue(self, **kw):
        data = json.loads(request.httprequest.data.decode("utf8"))
        _logger.info("API DATA %s" %data)
        error_item = ["Error Found: "]
        check_validation_errors = self.validate_fields(data)
        error_item += check_validation_errors
        if len(error_item) > 1:
            http.Response.status = "400"
            return {"status": "failure", "message": ',\n'.join(error_item)}
        try:
            helpdesk_ticket = request.env['helpdeskticket.model'].sudo()
            contact = data.get('contact_details')
            ticket_item = data.get('ticket_items')
            description = ticket_item.get('description')
            category_id = ticket_item.get('category_id')
            client_email = contact.get('client_email', 0)
            client_name = contact.get('client_name', 0)
            priority = ticket_item.get('priority')
            category_ref = request.env['helpdeskcategory.model'].sudo().browse([int(category_id)])
            vals = {
                'description': description,
                'category_id': category_id,
                'client_email': client_email,
                'client_name': client_name,
                'active': True,
                'priority': 'high' if priority == 1 else 'medium' if priority == 2 else 'low',
            }
            ticket_obj = helpdesk_ticket.sudo().create(vals)

            ticket_obj.send_mail(client_email, category_ref.email, True, None, False)
            http.Response.status = "201"
            return {
                "status": "successful",
                "ticket_data": [{'id': c.id, 'ticket_id': c.name, 'client_email': c.client_email} for c in ticket_obj]
            }
        except Exception as e:
            _logger.exception(e)
            http.Response.status = "400"
            return {"status": "failure", "message": str(e)}

