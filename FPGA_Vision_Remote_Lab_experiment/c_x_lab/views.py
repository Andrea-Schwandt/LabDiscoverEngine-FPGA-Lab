import os
import time
import cv2

from flask import Flask, Blueprint, url_for, render_template, jsonify, session, current_app, request, redirect, send_from_directory, Response
from werkzeug.utils import secure_filename

from c_x_lab import weblab
from c_x_lab.hardware import gen_frames, program_device, program_invert, program_filter, program_edge, measure, image_home, image_last, image_next, image_end

from labdiscoverylib import requires_active, requires_login, weblab_user, logout

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'

app = Flask(__name__)

main_blueprint = Blueprint('main', __name__)

@weblab.initial_url
def initial_url():
    """
    Where do we send the user when a new user comes?
    """
    return url_for('main.index')



@main_blueprint.route('/')
@requires_login
def index():
    # This method generates a random identifier and stores it in Flask's session object
    # For any request coming from the client, we'll check it. This way, we avoid
    # CSRF attacks (check https://en.wikipedia.org/wiki/Cross-site_request_forgery )
    session['csrf'] = weblab.create_token()

    return render_template("index.html", resource=os.environ.get('RESOURCE'))

@main_blueprint.route('/status')
@requires_active
def status():

    task = weblab.get_task(program_device)
    if task:
        current_app.logger.debug("Current programming task status: %s (error: %s; result: %s)", task.status, task.error, task.result)

    return jsonify(error=False, time_left=weblab_user.time_left)

@main_blueprint.route('/logout', methods=['POST'])
@requires_login
def logout_view():
    if not _check_csrf():
        return jsonify(error=True, message="Invalid JSON")

    if weblab_user.active:
        logout()

    return jsonify(error=False)

ALLOWED_EXTENSIONS = {'sof'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_blueprint.route('/uploads', methods=['GET', 'POST'])
@requires_active
def download_bit_file(fpga_file):
   if request.method == 'POST':
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No file selected')
           return redirect(request.url)
       if file and allowed_file(file.fpga_file):
           filename = secure_filename(file.fpga_file)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], fpga_file))
           #process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
           return redirect(url_for('uploaded_file', filename=fpga_file))
   return render_template('index.html')



@main_blueprint.route('/video_feed')
@requires_active
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main_blueprint.route('/fpga', methods=['POST'])
@requires_active
def fpga():
    if not _check_csrf():
        return jsonify(error=True, message="Invalid CSRF")

    code = request.values.get('code') or "code"

    # If there are running tasks, don't let them send the program
    if len(weblab.running_tasks):
        return jsonify(error=True, message="Other tasks being run")

    task = program_device.delay(code)

    # Playing with a task:
    current_app.logger.debug("New task! {}".format(task.task_id))
    current_app.logger.debug(" - Name: {}".format(task.name))
    current_app.logger.debug(" - Status: {}".format(task.status))

    # Result and error will be None unless status is 'done' or 'failed'
    current_app.logger.debug(" - Result: {}".format(task.result))
    current_app.logger.debug(" - Error: {}".format(task.error))

    return status()


@main_blueprint.route('/measure', methods=['POST'])
@requires_active
def measure_current():
    current = measure()
    return current

@main_blueprint.route('/prog_invert', methods=['POST'])
@requires_active
def prog_invert():
    message = program_invert()
    return message

@main_blueprint.route('/prog_filter', methods=['POST'])
@requires_active
def prog_filter():
    message = program_filter()
    return message

@main_blueprint.route('/prog_edge', methods=['POST'])
@requires_active
def prog_edge():
    message = program_edge()
    return message

@main_blueprint.route('/img_home', methods=['POST'])
@requires_active
def img_home():
    message = image_home()
    return message

@main_blueprint.route('/img_last', methods=['POST'])
@requires_active
def img_last():
    message = image_last()
    return message

@main_blueprint.route('/img_next', methods=['POST'])
@requires_active
def img_next():
    message = image_next()
    return message

@main_blueprint.route('/img_end', methods=['POST'])
@requires_active
def img_end():
    message = image_end()
    return message


#######################################################
#
#   Other functions
#

def _check_csrf():
    expected = session.get('csrf')
    if not expected:
        current_app.logger.warning("No CSRF in session. Calling method before loading index?")
        return False

    obtained = request.values.get('csrf')
    if not obtained:
        # No CSRF passed.
        current_app.logger.warning("Missing CSRF in provided data")
        return False

    return expected == obtained
