
# @app.after_request
# def log_the_status_code(response):
#     status_as_string = response.status
#     status_as_integer = response.status_code
#     logging.warning("status as string %s" % status_as_string)
#     logging.warning("status as integer %s" % status_as_integer)
#     return response