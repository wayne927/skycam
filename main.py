from flask import Flask, render_template, make_response
import os

app = Flask(__name__)

camera_root = '/home/pi/camera'
#camera_files = camera_root + '/files'

def list_dir(directory) :
    local_dir = camera_root + '/' + directory
    ls_list = sorted([x for x in os.listdir(local_dir) if (not (x == '.' or x == '..'))])
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

#@app.route("/files/<directory>/", methods=['GET'])
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


