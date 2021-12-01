import json
import logging
from odoo import _
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)


class APIController(http.Controller):

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
            category_ref = request.env['helpdeskcategory.model'].sudo().search(
                [('id', '=', int(category_id))], limit=1)
            if not category_ref:
                error_item.append(
                    "Category ID provide is not existing on the database \n ")
        return error_item
    
    @http.route("/api/v1/issues/categories", type="json", auth="public", methods=["GET"], csrf=False)
    def get_categories(self, **kw):
        response = {
            "status": "success"
        }
        helpdesk_categories = request.env['helpdeskcategory.model'].sudo().search([])
        http.Response.status = "201"
        return {
            "status": "successful",
            "ticket_data": [{'id': category.id, 'ticket_id': category.name} for category in helpdesk_categories]
        }

    @http.route("/api/v1/issues", type="json", auth="public", methods=["GET"], csrf=False)
    def get_issue(self, **kw):
        response = {
            "status": "success"
        }
        helpdesk_tickets = request.env['helpdeskticket.model'].sudo().search([])
        http.Response.status = "201"
        return {
            "status": "successful",
            "ticket_data": [{'id': ticket.id, 'ticket_id': ticket.name, 'client_email': ticket.client_email} for ticket in helpdesk_tickets]
        }

    @http.route("/api/v1/issues", type="json", auth="public", methods=["POST"], csrf=False)
    def create_issue(self, **kw):
        response = {
            "status": "success"
        }
        data = json.loads(request.httprequest.data.decode("utf8"))
        HelpdeskTicket = request.env['helpdeskticket.model'].sudo()
        _logger.info("API DATA %s" % data)
        # error_item = ["Error Found: "]
        # check_validation_errors = self.validate_fields(data)
        # error_item += check_validation_errors
        # if len(error_item) > 1:
        #     http.Response.status = "400"
        #     return {"status": "failure", "message": ',\n'.join(error_item)}
        try:
            vals = {
                'description': data.get("description"),
                'category': data.get("category"),
                'client_email': data.get("client_email"),
                'client_name': data.get("client_name"),
                'active': True,
                'priority': data.get("prioirity"),
            }
            ticket = HelpdeskTicket.create(vals)

            # ticket.send_mail(
            #     vals.get("client_email"), category_ref.email, True, None, False)
            http.Response.status = "201"
            return {
                "status": "successful",
                "ticket_data": [{'id': c.id, 'ticket_id': c.name, 'client_email': c.client_email} for c in ticket]
            }
        except Exception as e:
            _logger.exception(e)
            http.Response.status = "400"
            return {"status": "failure", "message": str(e)}
