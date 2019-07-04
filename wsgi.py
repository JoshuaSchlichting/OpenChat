from app import app as application
from app import socketio as socketapp


if __name__ == "__main__":
	#application.run()
	socketapp.run(app=application, host='0.0.0.0', log_output=True, debug=True)
