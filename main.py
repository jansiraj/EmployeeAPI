from flask import Flask
from __init__ import db


def create_app():
    main_app = Flask(__name__)
    main_app.config.from_object("config.Config")
    db.init_app(main_app)
    from employee import employee as employee_blueprint
    main_app.register_blueprint(employee_blueprint)
    return main_app


app = create_app()

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=False, host='0.0.0.0', port=8000)