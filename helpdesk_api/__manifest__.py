##############################################################################
#    Copyright (C) 2018 oeHealth. All Rights Reserved
#    EHA Clinic Extensions to oeHealth, Hospital Management Solutions


{
    'name': 'Helpdesk Issue Tracker',
    'version': '1.5',
    'author': "Maach Softwares / Maduka Chris Sopulu",
    'category': 'Helpdesk',
    'summary': 'Helpdesk support application',
    'depends': ['base', 'mail'],

    'description': "Helpdesk support application",
    "data": [
            'security/security_view.xml',
            'security/ir.model.access.csv',
            'data/email_template.xml',
            'sequence/sequence.xml',
            'views/helpdesk_ticket_view.xml',
            'views/dashboard_view.xml',
        ],

    'css': [],
    'js': [],
    'qweb': [

    ],
    "active": False,
    "images": ['images/cover_thumbnail.png'],
    'application': True,
    "sequence": 3,
}
