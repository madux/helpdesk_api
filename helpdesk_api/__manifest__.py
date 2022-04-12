##############################################################################
#    Copyright (C) 2018 oeHealth. All Rights Reserved
#    EHA Clinic Extensions to oeHealth, Hospital Management Solutions


{
    'name': 'Helpdesk Issue Tracker',
    'version': '14.0',
    'author': "Maach Softwares / Maduka Chris Sopulu",
    'category': 'Helpdesk',
    'summary': 'Helpdesk support application',
    'depends': [
        'base', 
        'mail',
        'website'
    ],

    'description': "Helpdesk support application",
    "data": [
            'security/security_view.xml',
            'security/ir.model.access.csv',
            'data/email_template.xml',
            'sequence/sequence.xml',
            'views/helpdesk_ticket_view.xml',
            'views/dashboard_view.xml',
            'views/helpdesk_templates.xml',
        ],

    'css': [],
    'js': [],
    'qweb': [

    ],
    "active": False,
    "images": ['images/main_cover.jpg'],
    'application': True,
    "sequence": 3,
}
