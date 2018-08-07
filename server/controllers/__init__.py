from flask import Flask


def init_controllers(app: Flask):
    from server.controllers import attendance_controller
    app.register_blueprint(attendance_controller.blueprint)
    from server.controllers import student_controller
    app.register_blueprint(student_controller.blueprint)
    from server.controllers import admin_controller
    app.register_blueprint(admin_controller.blueprint)
