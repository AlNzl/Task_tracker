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
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'data/default_stages.xml',
        'views/template.xml',
        'data/default_reference_book.xml',
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
