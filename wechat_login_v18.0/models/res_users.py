# wechat_login/models/res_users.py
from odoo import models, fields

class ResUsersWeChat(models.Model):
    _inherit = 'res.users'

    wechat_openid = fields.Char(string='微信 OpenID', index=True)