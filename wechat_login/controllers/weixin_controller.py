# controllers/weixin_controller.py

import logging
import requests
from odoo import http
from odoo.http import request
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class WeixinAuthController(http.Controller):

    WEIXIN_APPID = 'wx5d723cf60c17644d'
    WEIXIN_SECRET = '61b145de2c835a1924303dc1ccc8d646'

    def _get_wechat_ids(self, code):
        """获取微信身份标识（同时返回 openid 和 unionid）"""
        token_url = (
            f"https://api.weixin.qq.com/sns/oauth2/access_token?"
            f"appid={self.WEIXIN_APPID}&"
            f"secret={self.WEIXIN_SECRET}&"
            f"code={code}&"
            f"grant_type=authorization_code"
        )
        
        try:
            response = requests.get(token_url, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            # 获取两种ID（UnionID可能为空）
            openid = result.get('openid', '')
            unionid = result.get('unionid', '')
            
            if not openid:
                error_msg = result.get('errmsg', '未知错误')
                _logger.error("微信API错误: %s - %s", result.get('errcode'), error_msg)
                return None, None, f"微信API错误: {error_msg}"
                
            return openid, unionid, None
            
        except requests.exceptions.RequestException as e:
            _logger.exception("微信API请求异常")
            return None, None, f"网络请求异常: {str(e)}"
        except Exception as e:
            _logger.exception("处理微信响应时发生意外错误")
            return None, None, f"处理响应时出错: {str(e)}"

    @http.route('/weixin/callback', type='http', auth='public')
    def weixin_callback(self, code=None, **kwargs):
        if not code:
            return "<h2>❌ 微信授权失败：未收到授权码</h2>"
            
        _logger.info("收到微信授权码: %s", code)

        # 获取微信身份标识
        openid, unionid, error = self._get_wechat_ids(code)
        if error:
            return f"<h2>❌ {error}</h2>"
            
        _logger.info("获取到微信标识: OPENID=%s | UNIONID=%s", openid, unionid)

        # 查询绑定的Odoo用户（使用OpenID作为主标识）
        user = request.env['res.users'].sudo().search([
            ('wechat_openid', '=', openid)  # 保持使用OpenID查询
        ], limit=1)

        if user:
            # ✅ 执行Odoo登录流程
            redirect_url = f'/web?login={user.login}'
            session = request.session
            session['auth_login'] = user.login
            session['uid'] = user.id
            session['session_token'] = user._compute_session_token(session.sid)
            
            _logger.info("用户 %s 登录成功 (OPENID:%s)", user.login, openid)
            return request.redirect(redirect_url)
        else:
            _logger.warning("未找到绑定的用户 (OPENID:%s)", openid)
            
            # 关键修改：显示未绑定时返回OpenID值
            return f"""
            <div style="max-width:500px;margin:50px auto;padding:20px;border:1px solid #eee;font-family:Arial,sans-serif">
                <h2 style="color:#e74c3c">❌ 账号未经授权！</h2>
               
                
                <div style="background:#f9f9f9;padding:15px;margin:20px 0;border-radius:5px">
                    <h4 style="margin-top:0">微信身份标识</h4>
                    <p><code style="word-break:break-all">{openid}</code></p>
                </div>
                

            </div>
            """