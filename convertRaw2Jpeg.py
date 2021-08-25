# import os
# os.system("cd /Users/leshumphris/Desktop/SDCARD/")
# # os.system("for i in *.CR3; do sips -s format jpeg $i --out (basename $i .CR3).jpg; end")
# os.system("for i in *.CR3; do sips -s format jpeg $i --out \"${i%.*}.jpg\"; done")


import subprocess


directory = "/Users/leshumphris/Desktop/SDCARD"
cr3_to_jpg = "for i in *.CR3; do sips -s format jpeg $i --out \"${i%.*}.jpg\"; done"
# process = subprocess.run(cr3_to_jpg, cwd=directory, shell=True, check=True)
process = subprocess.Popen(cr3_to_jpg, cwd=directory, shell=True)

# from subprocess import popen
# process = subprocess.Popen("bash for i in {1..3}; do echo ${i}; done")
try:
    outs, errs = process.communicate(timeout=10)
except subprocess.TimeoutExpired as e:
    process.kill()
    outs, errs = process.communicate()
    print("Error: CR3 to Jpeg conversion timed out")