from flask import Flask
from flask import request
from subprocess import call
import time

app = Flask(__name__)

# AVR - YAMAHA HTR-4063

@app.route('/avr/on', methods=['POST'])
def avr_on():
    avr_send_ir_code("KEY_POWER")
    return

@app.route('/avr/off', methods=['POST'])
def avr_off():
    avr_send_ir_code("KEY_SLEEP")
    return

@app.route('/avr/input/<input>', methods=['POST'])
def avr_input(input):
    if (input != "hdmi1" or
        input != "hdmi2" or
        input != "hdmi3" or
        input != "hdmi4" or
        input != "audio1" or
        input != "audio2"):
            abort(400)
    
    formatted_input = input.uppercase()
    avr_send_ir_code("INPUT" + formatted_input)
    return

@app.route('/avr/volume/up', methods=['POST'])
def avr_volume_up():
    avr_send_ir_code("KEY_VOLUMEUP")

@app.route('/avr/volume/down', methods=['POST'])
def avr_volume_down():
    avr_send_ir_code("KEY_VOLUMEDOWN")

@app.route('/avr/volume/mute', methods=['POST'])
def avr_volume_mute():
    avr_send_ir_code("VOL_MUTE")


# PROJECTOR - BENQ W1070

@app.route('/projector/on', methods=['POST'])
def projector_on():
    projector_send_ir_code("KEY_POWER")

@app.route('/projector/off', methods=['POST'])
def projector_off():
    projector_send_ir_code("KEY_SUSPEND")
    time.sleep(0.5)
    projector_send_ir_code("KEY_SUSPEND")

@app.route('/projector/input/<input>', methods=['POST'])
def projector_input(input):
    if (input == "hdmi1"):
        projector_send_ir_code("HDMI-1")
    elif (input == "hdmi2"):
        projector_send_ir_code("HDMI-2")
    else:
        abort(400)

def avr_send_ir_code(code):
    call(["irsend", "SEND_ONCE", "RAV_YAMAHA-RAV294", code])

def projector_send_ir_code(code):
    call(["irsend", "SEND_ONCE", "BENQ_W1070", code])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)