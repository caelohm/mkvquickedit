import os, re, subprocess

if __name__ == "__main__":
    mkv_mp4_path = input('enter mkv file directory\nif ctrl+V doesn\'t work try ctrl+shift+V\n')
    sorting = input('sort by?\n')

    episodes = []

    for (dirpath, dirnames, filenames) in os.walk(mkv_mp4_path):
        for file in filenames:
            if (sorting != 'none'):
                if (re.search('.mkv', file) != None or re.search('.mp4', file) != None):
                    if (sorting != 'none' and re.search(sorting, dirpath) != None):
                        episodes.append(['', os.path.join(dirpath, file), ''])
    
    '''
    after mkvinfo, need name of .mkv file. Prints to terminal
    information about tracks. Keep all MB_per_Min and File name
    in a list and sort. Then write to the txt.
    '''

    for i in range(len(episodes)):
        
        '''
        p = subprocess.Popen(['C:\\Projects\\MKVPROPEDIT\\ffmpeg\\bin\\ffprobe.exe', '-v', 'error', '-show_entries', 'format=duration', epi], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        
        file = open('output.txt', 'w', encoding='utf-8')
        file.write(p.communicate()[1].decode('utf-8').replace('\n  ', ''))
        file.close()
        '''

        p = subprocess.check_output(['C:\\Projects\\MKVPROPEDIT\\ffmpeg\\bin\\ffprobe.exe', '-v', 'error', '-show_entries', 'format=duration', episodes[i][1]])

        file = open('output.txt', 'w')
        file.write(p.decode('utf-8'))
        file.close()
        
        file = open('output.txt', 'r')
        for line in file:
            if (re.search('\d+.\d+', line) != None):
                duration = re.search('\d+.\d+', line).group(0)
        
        num_bytes = float(os.path.getsize(episodes[i][1]))

        episodes[i][0] = str(float(num_bytes) / 1000000)

        episodes[i][2] = round((float(num_bytes) / 1000000) / (float(duration) / 60), 2)

        file.close()

    sorted = sorted(episodes, key=lambda x:x[2])


    file2 = open('MB_per_Min_' + sorting + '.txt', 'w')
    file2.write('MB/s  Total Megabytes  Episode Path\n')

    for val in sorted:
        file2.write(str(val[2]) + '     ' + val[0] + '    ' + val[1] + '\n')
    file2.close()
    
    # os.remove('output.txt')
    # tempf.close()
