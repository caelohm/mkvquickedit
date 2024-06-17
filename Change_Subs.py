import os, re, subprocess

if __name__ == "__main__":
    episodes = []

    mkv_path = input('enter mkv file directory\nif ctrl+V doesn\'t work try ctrl+shift+V\n')
    add_rem = input('0 for disable subtitles 1 for enable\n')
    while (add_rem != '0' and add_rem != '1'):
        add_rem = input('ERROR: must input 0 for disable subtitles or 1 for enable\n')

    for (dirpath, dirnames, filenames) in os.walk(mkv_path):
        for file in filenames:
            if (re.search('.mkv', file) != None):
                episodes += [os.path.join(dirpath, file)]
    
    '''
    after mkvinfo, need name of .mkv file. Prints to terminal
    information about tracks. Need to know the number of the 
    subtitle track in order to turn off the default tag for
    that subtitle track in that mkv file. We know it's a 
    subtitle track if the "Track type: subtitles" We look
    for "Track number: #" keyword as a start.
    '''
    # tempf = open('output2.txt', 'w')

    for epi in episodes:
        
        p = subprocess.check_output(['C:\\Program Files (x86)\\MKVToolNix\\mkvinfo.exe', epi])
        
        file = open('output.txt', 'w')
        file.write(p.decode('utf-8'))
        file.close()
        
        file = open('output.txt', 'r')
        for line in file:
            if (re.search('Track number:', line) != None):
                Tracknum = re.search('\d', line).group(0)

                '''
                Once we have the subtitle track number, turning off the default
                tag for that track is done with the following command:
                    mkvpropedit movie.mkv --edit track:1 --set flag-default=0
                '''

                line = file.readline()
                while (re.search('Track type:', line) == None):
                    line = file.readline()
                if (re.search('subtitles', line) != None):
                    subprocess.run(['C:\\Program Files (x86)\\MKVToolNix\\mkvpropedit.exe', epi, '--edit', 'track:' + Tracknum, '--set', 'flag-default=' + add_rem])
                    # tempf.write(epi + Tracknum + '\n')

        file.close()
    
    os.remove('output.txt')
    # tempf.close()
