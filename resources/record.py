from flask import Flask
from flask_restplus import Api, Resource, fields

from server.instance import server
from models.record import record

app, api = server.app, server.api

# Let's just keep them in memory 
records_db = [
    {"id": 0, "name": "Ashwini"},
    {"id": 1, "name": "Mushu"},
]

# This class will handle GET and POST to /records
@api.route('/records')
class recordList(Resource):
    @api.marshal_list_with(record)
    def get(self):
        return records_db

    # Ask flask_restplus to validate the incoming payload
    @api.expect(record, validate=True)
    @api.marshal_with(record)
    def post(self):
        # Generate new Id
        api.payload["id"] = records_db[-1]["id"] + 1 if len(records_db) > 0 else 0
        records_db.append(api.payload)
        return api.payload

# Handles GET and PUT to /records/:id
# The path parameter will be supplied as a parameter to every method
@api.route('/records/<int:id>')
class record(Resource):
    # Utility method
    def find_one(self, id):
        return next((b for b in records_db if b["id"] == id), None)

    @api.marshal_with(record)
    def get(self, id):
        match = self.find_one(id)
        return match if match else ("Not found", 404)

    @api.marshal_with(record)
    def delete(self, id):
        global records_db 
        match = self.find_one(id)
        records_db = list(filter(lambda b: b["id"] != id, records_db))
        return match

    # Ask flask_restplus to validate the incoming payload
    @api.expect(record, validate=True)
    @api.marshal_with(record)
    def put(self, id):
        match = self.find_one(id)
        if match != None:
            match.update(api.payload)
            match["id"] = id
        return match