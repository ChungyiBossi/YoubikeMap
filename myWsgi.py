from simple_app import create_flask_app
import logging

app = create_flask_app()  # for gunicorn
# gunicorn_logger = logging.getLogger('gunicorn.error')
# app.logger.handlers = gunicorn_logger.handlers