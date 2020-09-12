import subprocess
from datetime import datetime
import psutil
import os

def shutter_in_seconds(t) :
    return int(t * 1000000)
def timelapse_in_seconds(t) :
    return int(t * 1000)
def timelapse_in_minutes(t) :
    return int(t * 60 * 1000)

def parse_settings(settings) :
    command = ['/usr/bin/raspistill']
    for s,val in settings.items() :
        command.append('--'+str(s))
        if (val) :
            command.append(str(val))
    print(command)
    return command

def shoot(settings) :
    command = parse_settings(settings)
    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    # output is a binary string. Need decode to convert to ASCII
    return output.decode()

def timelapse(settings) :
    command = parse_settings(settings)
    with open('static/raspistill_out.txt', 'w') as out :
        subprocess.Popen(command, stdout=out, stderr=out)

def get_camera_pid() :
    pid = 0
    for p in psutil.process_iter(['pid', 'name', 'status']) :
        try :
            if (p.info['name'].lower() == 'raspistill') :
                print(p.info)
                if (p.info['status'] != psutil.STATUS_ZOMBIE) :
                    pid = p.info['pid']
                    break
        except :
            pass
    return pid

if __name__ == "__main__" :
    time_str = datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    filebase = 'pi'
    filename = filebase + '_' + time_str + '.jpg'

    settings = {'output': filename}

    settings['width'] = 2000
    settings['height'] = int(settings['width']/3280.0*2464.0)
    settings['rotation'] = 180
    settings['quality'] = 100
    settings['ISO'] = 800
    settings['shutter'] = shutter_in_seconds(0.1)
    settings['verbose'] = ""

    shoot(settings)
