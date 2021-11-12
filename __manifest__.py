{
    'name': "Task Tracker",
    'description': 'Chto-to',
    'author': 'depressed tilted',
    'depends': ['hr'],
    'data': [
        'data/default_stages.xml',
        'view/hr_employee_view.xml',
        'view/task_view.xml',
        'view/project_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True
}
