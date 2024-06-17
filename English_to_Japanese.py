import os, re, subprocess

if __name__ == "__main__":
    episodes = []

    mkv_path = input('enter mkv file directory\nif ctrl+V doesn\'t work try ctrl+shift+V\n')

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
    # tempf.write(epi + Tracknum + '\n')


    for epi in episodes:
        
        p = subprocess.check_output(['C:\\Program Files (x86)\\MKVToolNix\\mkvinfo.exe', epi])
        
        p = p.decode('utf-8').replace('\n|', '')

        file = open('output.txt', 'w')
        file.write(p)
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
                line = file.readline()

                if (re.search('Track type: audio', line) != None):
                    for i in range(8):
                        if (re.search('Language', line) == None):
                            line = file.readline()
                    
                    if (re.search('en', line) != None):
                        # turn english audio off
                        subprocess.run(['C:\\Program Files (x86)\\MKVToolNix\\mkvpropedit.exe', epi, '--edit', 'track:' + Tracknum, '--set', 'flag-default=0'])
                    elif (re.search('ja', line) != None):
                        # turn japanese audio on
                        subprocess.run(['C:\\Program Files (x86)\\MKVToolNix\\mkvpropedit.exe', epi, '--edit', 'track:' + Tracknum, '--set', 'flag-default=1'])
                    else:
                        print('Problem with audio track, couldn\'t find language.')


                elif (re.search('Track type: subtitles', line) != None):
                    for i in range(8):
                        if (re.search('Language', line) == None):
                            line = file.readline()

                    if (re.search('en', line) != None):
                        line = file.readline()
                        # make sure it's not a Signs or Songs subtitle file
                        if (re.search('(S|s)igns|(S|s)ongs', line) == None):
                            # turn english subtitles on
                            subprocess.run(['C:\\Program Files (x86)\\MKVToolNix\\mkvpropedit.exe', epi, '--edit', 'track:' + Tracknum, '--set', 'flag-default=1'])
                        else:
                            # disable Signs & Songs subtitle files
                            subprocess.run(['C:\\Program Files (x86)\\MKVToolNix\\mkvpropedit.exe', epi, '--edit', 'track:' + Tracknum, '--set', 'flag-default=0'])
                    else:
                        print('Problem with subtitles, couldn\'t find language.')
                        
        file.close()
    
    
    # os.remove('output.txt')
    # tempf.close()
