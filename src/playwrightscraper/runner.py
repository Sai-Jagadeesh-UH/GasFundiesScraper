from .main import gui_app
import gevent.pywsgi

app_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 8088), gui_app)
app_server.serve_forever()
