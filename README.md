# helpdesk_api
This module provide feature to help you Track issues from Clients/ Customers. It also comes with an easy to connect api connector that be consumed by any application.

For configuration: Simply Install the module "helpdesk_api". Open the module, click on configuration. Setup the stages and categories.

To generate a ticket on the odoo view: Click on helpdesk Issue Tracker Module 'Create a ticket' Add the required fields and save. -We provided a dynamic email feature to send mail when issues are dragged from one stage to another

Also you can add or assign to multiple team. For External API use:

Ensure your Json payload is as follows; .

'{

"contact_details": {

  'client_name': "Ebuka Chinedu", 
  'client_email': "Ebuka Chinedu", 
  'client_phone': "+2347067979346"
  }, 
"ticket_items": {

  "description": "Request for a fix...", 
  "category_id": 1, 
  "priority": 1', #1 high, 2 medium, 3 low
  }
}'

API Link: 'https://yourhostname/api/v1/issue/create'
