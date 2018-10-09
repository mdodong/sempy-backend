from flask import  redirect, url_for
import connexion
from flask_cors import CORS
import app.api

# Create the application instance
app = connexion.App(__name__, specification_dir='api/')


# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.json', swagger_ui=True)

# add CORS support
CORS(app.app)

# Create a URL route in our application for "/"
#flask_app = app.app
from app.explorer.routes import mod
app.app.register_blueprint(mod)
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
