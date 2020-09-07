from flask import Flask, render_template, make_response
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
    return render_template('index.html')

@app.route("/shoot")
def take_pic() :
    time_str = datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    filebase = 'pi'
    filename = filebase + '_' + time_str + '.jpg'

    settings = {'output': camera_root + '/files/' + filename}
    settings['width'] = 2000
    settings['height'] = int(settings['width']/3280.0*2464.0)
    settings['rotation'] = 180
    settings['quality'] = 100
    settings['ISO'] = 800
    settings['shutter'] = camera.shutter_in_seconds(1)
    settings['verbose'] = ""

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


