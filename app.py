from flask import Flask
from flask import request
from flask import abort
from subprocess import call
import time

app = Flask(__name__)

# AVR - YAMAHA HTR-4063

@app.route('/avr/power', methods=['POST'])
def avr_on():
    avr_send_ir_code("KEY_POWER")
    return ''

@app.route('/avr/input/<input>', methods=['POST'])
def avr_input(input):
    if (input != "hdmi1" and
        input != "hdmi2" and
        input != "hdmi3" and
        input != "hdmi4" and
        input != "audio1" and
        input != "audio2"):
            abort(400)
    
    formatted_input = input.upper()
    avr_send_ir_code("INPUT" + formatted_input)
    return ''

@app.route('/avr/volume/up', methods=['POST'])
def avr_volume_up():
    avr_send_ir_code("KEY_VOLUMEUP")
    return ''

@app.route('/avr/volume/down', methods=['POST'])
def avr_volume_down():
    avr_send_ir_code("KEY_VOLUMEDOWN")
    return ''

@app.route('/avr/volume/mute', methods=['POST'])
def avr_volume_mute():
    avr_send_ir_code("VOL_MUTE")
    return ''


# PROJECTOR - BENQ W1070

@app.route('/projector/on', methods=['POST'])
def projector_on():
    projector_send_ir_code("KEY_POWER")
    return ''

@app.route('/projector/off', methods=['POST'])
def projector_off():
    projector_send_ir_code("KEY_SUSPEND")
    time.sleep(0.5)
    projector_send_ir_code("KEY_SUSPEND")
    return ''

@app.route('/projector/input/<input>', methods=['POST'])
def projector_input(input):
    if (input == "hdmi1"):
        projector_send_ir_code("HDMI-1")
    elif (input == "hdmi2"):
        projector_send_ir_code("HDMI-2")
    else:
        abort(400)
    
    return ''

def avr_send_ir_code(code):
    call(["irsend", "SEND_ONCE", "YAMAHA-RAV294", code])

def projector_send_ir_code(code):
    call(["irsend", "SEND_ONCE", "BENQ_W1070", code])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)