# helpdesk_api
This module provide feature to help you Track issues from Clients/ Customers. It also comes with an easy to connect api connector that be consumed by any application.

For configuration: Simply Install the module "helpdesk_api". Open the module, click on configuration. Setup the stages and categories.

To generate a ticket on the odoo view: Click on helpdesk Issue Tracker Module 'Create a ticket' Add the required fields and save. -We provided a dynamic email feature to send mail when issues are dragged from one stage to another

Also you can add or assign to multiple team. 

For External API use:
CREATE TICKET API: 
API Link: 'https://yourhostname/api/v1/issue/create'

GET CATEGORY API: 
## 

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
Contact details data is a dictionary that contacts information required for the application to 
generate a heldesk ticket record.

client_name is a required option; this is the field that holds the client Name
client_email is a required option; this is the field that holds the client Email
client_phone is a required option; this is the field that holds the client Phnone number
Ticket items data is the key that holds ticket details

description is required; this is the field that holds the description
category_id is not required; this is the field that holds the ticket category, you can call using the second api to get list of all category and map the ID (int) as the value
eg . 'category': 1, 1 is an example of a unique key which represents a record in the category table

priority is a selection ooption which just three options namely high, medium and low,
Low is the default option
While using the api, kindly ensure you use 1, 2  or 3 for either high, medium or low respectively
example: 
if you are making a call to create a ticket with high priority use
"priority": 1',




API TEST USING PYTHON REQUEST LIB

import json
import requests as rq
from datetime import datetime


parameter = {
        "contact_details": {
            'client_name': "Ebuka Chinedu", 
            'client_email': "ebuka@gmail.com", 
            'client_phone': "+2347067979346", 
            },
        "ticket_items": { 
            "description": "Request for a fix...",
            "category_id": 1,
            "priority": 1, #1 high,  2 medium, 3 low
        }

    }
json_headers = {
                "Content-Type": "application/json",
                'Accept':'application/json',
                 
                }
json_data = json.dumps(parameter)
localhost = "http://127.0.0.1:8070/api/v1/issue/create"
req = rq.post(localhost, data=json_data,
              headers=json_headers)
print(req)
print(req.content)
