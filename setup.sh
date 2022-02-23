# export FLASK_APP=simple_app
# export FLASK_ENV=development
# flask run --debugger

gunicorn  \
--access-logformat "{'remote_ip':'%(h)s','request_id':'%({X-Request-Id}i)s','response_code':'%(s)s','request_method':'%(m)s','request_path':'%(U)s','request_querystring':'%(q)s','request_timetaken':'%(D)s','response_length':'%(B)s'}" \
--reload \
--log-level=debug \
wsgi:app