import subprocess
from datetime import datetime
import psutil
import os, signal

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

def kill() :
    pid = get_camera_pid()
    if (pid == 0) :
        return 'raspistill not running. pid = 0'
    else :
        os.kill(pid, signal.SIGTERM)
        return 'Process ' + str(pid) + ' killed'

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

def get_camera_temperature() :
    output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
    cpu_temp = round(float(output.decode()) / 1000.0, 1)

    output = subprocess.check_output(['vcgencmd', 'measure_temp'])
    gpu_temp = output.decode()
    gpu_temp = gpu_temp.split('=')[1].split('\'')[0]

    return "CPU: " + str(cpu_temp) + "&#176C, GPU: " + str(gpu_temp) + "&#176C"

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
