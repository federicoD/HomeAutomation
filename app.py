from flask import Flask
from flask import request, Response
from flask import abort
from flask import jsonify
from functools import wraps
import settings
import subprocess
import time

app = Flask(__name__)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# AVR - YAMAHA HTR-4063

@app.route('/avr/power', methods=['POST'])
@requires_auth
def avr_on():
    avr_send_ir_code("KEY_POWER")
    return ''

@app.route('/avr/input/<input>', methods=['POST'])
@requires_auth
def avr_input(input):
    if (input != "hdmi1" and
        input != "hdmi2" and
        input != "hdmi3" and
        input != "hdmi4" and
        input != "audio1" and
        input != "audio2"):
            abort(400, 'Invalid input. Supported hdmi1/2/3/4 or audio1/2')
    
    formatted_input = input.upper()
    avr_send_ir_code("INPUT " + formatted_input)
    return ''

@app.route('/avr/volume/up', methods=['POST'])
@requires_auth
def avr_volume_up():
    avr_send_ir_code("KEY_VOLUMEUP")
    return ''

@app.route('/avr/volume/down', methods=['POST'])
@requires_auth
def avr_volume_down():
    avr_send_ir_code("KEY_VOLUMEDOWN")
    return ''

@app.route('/avr/volume/mute', methods=['POST'])
@requires_auth
def avr_volume_mute():
    avr_send_ir_code("VOL_MUTE")
    return ''


# PROJECTOR - BENQ W1070

@app.route('/projector/on', methods=['POST'])
@requires_auth
def projector_on():
    projector_send_ir_code("KEY_POWER")
    return ''

@app.route('/projector/off', methods=['POST'])
@requires_auth
def projector_off():
    projector_send_ir_code("KEY_SUSPEND")
    time.sleep(0.5)
    projector_send_ir_code("KEY_SUSPEND")
    return ''

@app.route('/projector/input/<input>', methods=['POST'])
@requires_auth
def projector_input(input):
    if (input == "hdmi1"):
        projector_send_ir_code("HDMI-1")
    elif (input == "hdmi2"):
        projector_send_ir_code("HDMI-2")
    else:
        abort(400, 'invalid input. Supported: hdmi1/2')
    
    return ''

def avr_send_ir_code(code):
    try:
        #call(["irsend", "SEND_ONCE", "YAMAHA-RAV294", code])
        subprocess.check_output(["irsend", "SEND_ONCE", "YAMAHA-RAV294", code])
    except subprocess.CalledProcessError as e:
        abort(400, e.message)
    except Exception as e:
        abort(500, e.message)

def projector_send_ir_code(code):
    try:
        #call(["irsend", "SEND_ONCE", "BENQ_W1070", code])
        subprocess.check_output(["irsend", "SEND_ONCE", "BENQ_W1070", code])
    except subprocess.CalledProcessError as e:
        abort(400, e.message)
    except Exception as e:
        abort(500, e.message)

# @app.errorhandler(400)
# def custom400(error):
#     response = jsonify({'message': error})
#     return response

# @app.errorhandler(500)
# def custom500(error):
#     response = jsonify({'message': error})
#     return response

def check_auth(username, password):
    return username == settings.AUTH_USERNAME and password == settings.AUTH_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.PORT, debug=settings.DEBUG)