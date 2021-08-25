from PIL import Image
import os.path, time, stat

def get_date_taken(file_path):
    # return Image.open(path)._getexif()[36867]
    # return Image.open(file_path)._getexif()

    accessTimesinceEpoc = os.path.getmtime(file_path)
    return time.strftime('%Y%m%d', time.localtime(accessTimesinceEpoc))


if __name__ == "__main__":
    file = '/Users/leshumphris/Desktop/SDCARD/LES_0574.CR3'
    # date_time = get_date_taken('/Users/leshumphris/Desktop/SDCARD/LES_1071.CR3')
    # date = (date_time.split()[0]).replace(':', '')
    # print(date)

    # print("created: %s" % time.ctime(os.path.getctime('/Users/leshumphris/Desktop/SDCARD/LES_1071.CR3')))
    # exit(1)
    # Get last access time of file in seconds since epoch
    # accessTimesinceEpoc = os.path.getctime(file)
    # # convert time sinch epoch to readable format
    # # accessTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(accessTimesinceEpoc))
    # accessTime = time.strftime('%Y%m%d', time.localtime(accessTimesinceEpoc))
    # print(accessTime)

    print(get_date_taken(file))