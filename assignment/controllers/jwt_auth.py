# controllers/jwt_auth.py
import jwt
import datetime
from odoo16 import http
from odoo16.http import request

class JwtAuthController(http.Controller):

    secret_key = "your_secret_key"  # Replace with a strong secret key

    @http.route('/api/authenticate', type='json', auth='none', methods=['POST'], csrf=False)
    def authenticate(self, **kwargs):
        # Get the credentials from the request
        login = kwargs.get('login')
        password = kwargs.get('password')

        # Authenticate user using Odoo's authentication method
        uid = request.session.authenticate(request.db, login, password)
        if uid:
            # Generate a JWT token
            token = jwt.encode({
                'user_id': uid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expiry time
            }, self.secret_key, algorithm="HS256")

            return {'token': token}

        return {'error': 'Invalid credentials'}, 401

    def _check_jwt_token(self):
        token = request.httprequest.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
                uid = payload.get('user_id')
                user = request.env['res.users'].sudo().browse(uid)
                if user:
                    request.uid = uid
                    return True
            except jwt.ExpiredSignatureError:
                return False
            except jwt.InvalidTokenError:
                return False
        return False

    @http.route('/api/protected-route', type='json', auth='none', methods=['GET'], csrf=False)
    def protected_route(self, **kwargs):
        # Use the JWT validation method before processing
        if not self._check_jwt_token():
            return {'error': 'Unauthorized'}, 401

        # Logic for authenticated users
        return {'message': 'You have access to this route'}
