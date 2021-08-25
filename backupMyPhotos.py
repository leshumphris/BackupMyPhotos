
'''
Import photos from SD card into folder with date + nickname
Use: backupMyPhotos.py <nickname of folder (optional)>
Add script to to path
'''

import os
import sys
import shutil
import os.path, time
import subprocess

FNULL = open(os.devnull, 'w')
#16/11/2020
# Insert appropriate path and files extention.
sd_photo_folder = '/Users/leshumphris/Desktop/Raw/' # example: '/media/mycard/disk/DCIM/'
hdd_folder = '/Users/leshumphris/Desktop/'
file_extension = '.CR3' # example: '.ORF', '.jpg' or '.CR2'
folder_name = sys.argv[1] if len(sys.argv) == 2 else ''


# Print iterations progress
# From this SO answer: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/15862022
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def getDateOfPhoto(file_path):
    access_time_since_epoc = os.path.getmtime(file_path)
    return time.strftime('%Y%m%d', time.localtime(access_time_since_epoc))


def createOutputFolder(output_folder):
    try:
        os.makedirs(output_folder)
        return True
    except FileExistsError as exists:
        print('Folder exists:', exists.filename)
        print('Using existing folder...')
        return False


def checkIfFolderExists(folder, directory):
    files = os.listdir(directory)
    return True if folder not in files else False



def copyPhotos(sd_photo_folder, hdd_folder, file_extension='', folder_name=''):
    sd_files = os.listdir(sd_photo_folder)
    photo_dates = set()
    new_folders = set()

    #Filter for raw extension
    selected_files = [k for k in sd_files if k.endswith(file_extension)]
    n_files = len(selected_files)

    print('Copying', n_files, 'photos from SD card to', hdd_folder)

    printProgressBar(0, n_files, prefix = 'Copying photos:', suffix = '', length = 50)

    for i, file_name in enumerate(selected_files):
        printProgressBar(i + 1, n_files, prefix = 'Progress:', suffix = '', length = 50)
        date = getDateOfPhoto(sd_photo_folder + file_name)

        if date not in photo_dates:
            new_folder = date + '_' + folder_name if folder_name is not '' else date
            is_new_folder = createOutputFolder(hdd_folder + new_folder)
            if is_new_folder: new_folders.add(new_folder)

        photo_dates.add(date)

        try:
            shutil.copy(os.path.join(sd_photo_folder, file_name), hdd_folder + new_folder)
            shutil.copystat(os.path.join(sd_photo_folder, file_name), os.path.join(hdd_folder, new_folder, file_name))
        except:
            print("Error: Cannot copy file %s" % (hdd_folder + new_folder))
            exit(1)

    print('New folders added to %s:' % (hdd_folder), ', '.join(new_folders) if new_folders else "None")

    return new_folders, selected_files


def convertRaw2Jpeg(directory, new_folder, file_extension):
    command_1 = "for i in *{}; ".format(file_extension)
    command_2 = "do sips -s format jpeg $i --out \"{}/".format(new_folder)
    command_3 = "${i%.*}.jpg\" &> /dev/null; done"
    cr3_to_jpg = command_1 + command_2 + command_3

    process = subprocess.Popen(cr3_to_jpg, cwd=directory, stdout=FNULL, shell=True)
    try:
        # outs, errs = process.communicate(timeout=20)
        outs, errs = process.communicate()
    except subprocess.TimeoutExpired as e:
        process.kill()
        # outs, errs = process.communicate()
        print("Error: CR3 to Jpeg conversion timed out")
        # print(outs, errs)


def ProcessJpegsIntoFolders(folders):
    n_folders = len(folders)
    print('Going through the', n_folders, 'new folders and creating jpegs...')

    printProgressBar(0, n_folders, prefix='Converting photos:', suffix='', length=50)

    for i, folder in enumerate(folders):
        printProgressBar(i + 1, n_folders, prefix='Progress:', suffix='', length=50)
        new_folder = hdd_folder + folder + "/Jpegs"
        createOutputFolder(new_folder)
        convertRaw2Jpeg(hdd_folder + folder, 'Jpegs', file_extension)


folders, files = copyPhotos(sd_photo_folder, hdd_folder, file_extension, folder_name)
ProcessJpegsIntoFolders(folders)

