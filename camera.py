import subprocess
from datetime import datetime

def shoot(settings) :
    command = ['/usr/bin/raspistill']
    for s,val in settings.items() :
        command.append('--'+str(s))
        if (val) :
            command.append(str(val))

    print(command)

    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    return output.decode()

def shutter_in_seconds(t) :
    return int(t * 1000000)

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
