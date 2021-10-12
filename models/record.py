from flask_restplus import fields
from server.instance import server

record = server.api.model('Record', {
    'id': fields.Integer(description='Id'),
    'name': fields.String(required=True, min_length=1, max_length=200, description='Enter_name')
})