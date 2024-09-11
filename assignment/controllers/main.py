from odoo import http
from odoo.http import request
import jwt
import datetime
import base64

SECRET_KEY = 'your_secret_key'

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None

class ApiController(http.Controller):

    @http.route('/api/customer/login', auth='public', methods=['POST'], csrf=False)
    def customer_login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = request.env['res.users'].sudo().search([('login', '=', username), ('password', '=', password)], limit=1)
        if user:
            token = generate_jwt(user.id)
            return {'token': token}
        return {'error': 'Invalid credentials'}, 401

    @http.route('/api/customer/logout', auth='public', methods=['POST'], csrf=False)
    def customer_logout(self, **kwargs):
        # Token invalidation logic can be added here
        return {'status': 'Logged out successfully'}

    @http.route('/api/order', auth='public', methods=['GET', 'POST'], csrf=False)
    @http.route('/api/order/<int:order_id>', auth='public', methods=['GET', 'PUT', 'DELETE'], csrf=False)
    def manage_orders(self, order_id=None, **kwargs):
        if order_id:
            order = request.env['sale.order'].sudo().browse(order_id)
            if kwargs.get('method') == 'PUT':
                # Update order
                order.write(kwargs)
            elif kwargs.get('method') == 'DELETE':
                # Delete order
                order.unlink()
            return request.make_response(order.read())
        else:
            if kwargs.get('method') == 'POST':
                # Create new order
                order = request.env['sale.order'].sudo().create(kwargs)
                return request.make_response(order.read())
            else:
                # List all orders
                orders = request.env['sale.order'].sudo().search([])
                return request.make_response(orders.read())

    @http.route('/api/order/<int:order_id>/payments', auth='public', methods=['GET'], csrf=False)
    def track_payments(self, order_id, **kwargs):
        order = request.env['sale.order'].sudo().browse(order_id)
        payments = request.env['account.payment'].sudo().search([('sale_order_id', '=', order.id)])
        return request.make_response(payments.read())

    @http.route('/api/order/invoice/<int:invoice_id>', auth='public', methods=['GET'], csrf=False)
    def fetch_invoice(self, invoice_id, **kwargs):
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        pdf = request.env.ref('account.report_invoice').sudo().render_qweb_pdf([invoice.id])[0]
        pdf_base64 = base64.b64encode(pdf).decode('utf-8')
        return request.make_response(pdf_base64, headers=[('Content-Type', 'application/pdf')])
