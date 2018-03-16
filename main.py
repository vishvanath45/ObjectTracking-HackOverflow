import re
import subprocess
import math
from playsound import playsound

cellNumberRe = re.compile(r"^Cell\s+(?P<cellnumber>.+)\s+-\s+Address:\s(?P<mac>.+)$")
regexps = [
    re.compile(r"^ESSID:\"(?P<essid>.*)\"$"),
    re.compile(r"^Frequency:(?P<frequency>[\d.]+) (?P<frequency_units>.+) \(Channel (?P<channel>\d+)\)$"),
    re.compile(r"^Quality=(?P<signal_quality>\d+)/(?P<signal_total>\d+)\s+Signal level=(?P<signal_level_dBm>.+) d.+$"),
    re.compile(r"^Signal level=(?P<signal_quality>\d+)/(?P<signal_total>\d+).*$"),
]

def scan(interface='wlan0'):
    cmd = ["iwlist", interface, "scan"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    points = proc.stdout.read().decode('utf-8')
    return points

def parse(content):
    cells = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        cellNumber = cellNumberRe.search(line)
        if cellNumber is not None:
            cells.append(cellNumber.groupdict())
            continue
        for expression in regexps:
            result = expression.search(line)
            if result is not None:
                cells[-1].update(result.groupdict())
                continue
    return cells


def main():

    # macids = list()

    macids = str('A4:70:D6:78:B0:0D')
    device_id = str('wlx20e61600ce7e')

    pp = 5
    while(1):
        pp += 1

        content = scan(interface=device_id)
        cells = parse(content)

        # print type(cells)
        for i in cells:

            if(str(i['mac'])==macids):
                # print "\n"
                # here this is in GHz, converting to MHz by multiplying 1000.
                freq_val = float(i['frequency'])*1000
                sig_lvl_dbm = float(i['signal_level_dBm'])

                distance = (27.55 - (20 * math.log(freq_val,10)) + abs(sig_lvl_dbm))/20;

                distance = math.pow(10.0, distance)

                if(1):
                    # print "alert !!! "
                    print "Name         : ", i['essid']
                    print "Frequency is : ", i['frequency']
                    print "Sig_lvl_dbm  : ", i['signal_level_dBm']
                    print "mac id       : ", i['mac']
                    print "distance is  : ", distance, " mtrs\n"
                    # if(distance > 5):
                        # print "dis more !!"
                        # playsound('BombSound.mp3')



if __name__ == "__main__":
    main()

