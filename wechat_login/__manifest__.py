{
    'name': '微信登录',
    'version': '1.0',
    'category': 'Website',
    'summary': '支持通过微信扫码登录 Odoo',
    'depends': ['base', 'web', 'auth_oauth'],
    'data': [
        'views/login_template.xml',
    ],
    'installable': True,
    'application': False,
    'controllers': [
        'controllers/weixin_controller',
    ],
}