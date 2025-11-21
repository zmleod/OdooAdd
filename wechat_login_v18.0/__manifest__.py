{
    'name': '微信登录',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'images': ['static/description/cover.png'], 
    'license': 'LGPL-3', 
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