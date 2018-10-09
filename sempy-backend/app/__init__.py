from flask import  redirect, url_for
import connexion
from flask_cors import CORS
import app.api

# Create the application instance
app = connexion.App(__name__, specification_dir='api/')


# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.json')

# add CORS support
CORS(app.app)

# Create a URL route in our application for "/"
flask_app = app.app
from app.explorer.routes import mod
flask_app.register_blueprint(mod)
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    flask_app.run(debug=True)
'''
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
'''
