from werkzeug.security import check_password_hash
from flask_restful import Resource
from server.database import db
from server.common.error_codes_and_messages import INVALID_USERNAME_OR_PASSWORD
from server.database.models.user import User
from .models.authentication import Authentication, AuthenticationSchema
from .models.authentication_credentials import AuthenticationCredentialsSchema
from .decorators import unmarshal_request, marshal_response
from .helpers.authenticate import generate_api_key


class Authenticate(Resource):
    @unmarshal_request(AuthenticationCredentialsSchema())
    @marshal_response(AuthenticationSchema())
    def post(self, model):
        user = db.session.query(User).filter_by(
            username=model.username).first()

        if not user or not check_password_hash(user.password, model.password):
            return INVALID_USERNAME_OR_PASSWORD

        if not user.api_key:
            user.api_key = generate_api_key()
            db.session.add(user)
            db.session.commit()

        result = Authentication(
            http_header="apiKey", http_header_value=user.api_key)
        return result
