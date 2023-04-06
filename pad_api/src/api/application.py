from flasgger import Swagger
from flask import Flask, request, redirect
from flask.json import jsonify
from marshmallow import ValidationError

# Construct and configure the Flask application
api = Flask(__name__)

# Construct and configure the Swagger documentation
doc_config = {
    "info": {
        "title": "Journal Observatory - Platform Assertion Document API",
        "description": (
            "This REST endpoint provides an alternative endpoint to the "
            "Journal Observatory Platform Assertion Document "
            f"[SPARQL endpoint]({api.config.get('sparql_endpoint')})."
        ),
        "version": "0.0.1"
    }
}
doc = Swagger(api, template=doc_config)

@api.route('/')
@api.route('/api')
def apidocs():
    return redirect('/apidocs')

# PAD api endpoint
from api.pad import PADView, PADSubView
api.add_url_rule("/pad/<id>", view_func=PADView.as_view("pad_id"))
api.add_url_rule("/pad/<id>/<sub>", view_func=PADSubView.as_view("pad_sub"))

# PADs api endpoint
from api.pads import PADsView, PADsIdView
api.add_url_rule("/pads", view_func=PADsView.as_view("pads"))
api.add_url_rule("/pads/<id>", view_func=PADsIdView.as_view("pads_id"))

# Error handling
@api.errorhandler(400)
@api.errorhandler(401)
@api.errorhandler(404)
@api.errorhandler(500)
def httperrorhandler(e):
    if request.args.get("format", "") in ("ttl", "trig", "html"):
        return f"<pre>{str(e.description)}</pre>"
    if request.headers.get("Accept", "") in ("text/html"):
        return f"<pre>{str(e.description)}</pre>"
    return jsonify({"message": str(e.description)})

@api.errorhandler(ValidationError)
def validationerrorhandler(e):
    if request.args.get("format", "") in ("ttl", "trig", "html"):
        return f"<pre>{str(e)}</pre>"
    if request.headers.get("Accept", "") in ("text/html"):
        return f"<pre>{str(e)}</pre>"
    return jsonify({"message": str(e)}), 400
