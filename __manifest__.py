{
    'name': 'Task Tracker',
    'version': '1.1',
    'summary': '',
    'sequence': 1,
    'description': 'Task tracker',
    'category': '',
    'website': '',
    'images': [
    ],
    'depends': ['base', 'hr'],
    'data': [
        'data/default_stages.xml',
        'security/ir.model.access.csv',
        'views/task_view.xml',
        'views/project_view.xml',
        'views/hr_employee_view.xml',
        'views/reference_book_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
