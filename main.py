from flask import Flask, render_template, make_response, request
import os
from datetime import datetime
import camera

app = Flask(__name__)

camera_root = '/home/pi/camera'
#camera_files = camera_root + '/files'

def list_dir(directory) :
    local_dir = camera_root + '/' + directory
    ls_list = [local_dir + '/' + x for x in os.listdir(local_dir) if (not (x == '.' or x == '..'))]
    ls_list.sort(key=os.path.getmtime, reverse=True)
    ls_list = [os.path.basename(x) for x in ls_list]
    dir_list =   [x for x in ls_list if os.path.isdir(local_dir + '/' + x)]
    files_list = [x for x in ls_list if x not in dir_list]

    return render_template('files.html', files=files_list, dirs=dir_list, current_dir=directory)
    
def returnfile(filename) :
    infile = open(camera_root + '/' + filename, 'rb')
    data = infile.read()
    infile.close()

    response = make_response(data)
    response.headers.set('Content-Type', 'image/jpeg')

    return response

@app.route("/")
def home() :
    return app.send_static_file('index.html')

@app.route("/timelapse")
def take_timelapse() :
    camera.timelapse()
    return "timelapse return"

def setting_is_valid(setting) :
    return (setting and not setting.isspace())

@app.route("/shoot", methods=['POST'])
def take_pic() :
    if (not request.form) :
        return "Error in form"

    if (not setting_is_valid(request.form['filename'])) :
        return "Error in file name"
    else :
        filebase = request.form['filename']

    time_str = datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    filename = filebase + '_' + time_str + '.jpg'

    settings = {'output': camera_root + '/files/' + filename}
    settings['verbose'] = ""

    if (setting_is_valid(request.form['width'])) :
        settings['width'] = request.form['width']

    if (setting_is_valid(request.form['height'])) :
        settings['height'] = request.form['height']

    if (setting_is_valid(request.form['rotation'])) :
        settings['rotation'] = request.form['rotation']

    if (setting_is_valid(request.form['quality'])) :
        settings['quality'] = request.form['quality']

    if (setting_is_valid(request.form['sharpness'])) :
        settings['sharpness'] = request.form['sharpness']

    if (setting_is_valid(request.form['ISO'])) :
        settings['ISO'] = request.form['ISO']

    if (setting_is_valid(request.form['shutter'])) :
        settings['shutter'] = camera.shutter_in_seconds(float(request.form['shutter']))

    output = camera.shoot(settings)
    output = output.replace('\n', '<br>')
    return render_template('shoot.html', pic_file='files/'+filename, command_output=output)

@app.route("/<path:req_path>")
def show(req_path) :
    req_path = req_path.strip('/')
    if (os.path.isdir(camera_root + '/' + req_path)) :
        return list_dir(req_path)
    elif (req_path[-4:].lower() == '.jpg') :
        return returnfile(req_path)    
    else :
        return "Path not found"
    


if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True, port=80)


