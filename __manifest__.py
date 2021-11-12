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
        'view/stage_view.xml',
        'view/task_view.xml',
        'view/hr_employee_view.xml',
        'view/project_view.xml',
        'security/ir.model.access.csv',
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
