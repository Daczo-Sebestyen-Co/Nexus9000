import os

folder = "Prototype_keyb/final"

try:
    #os.system("rshell")
    for e in os.listdir(folder):
        os.system(f"rshell cp {folder}/{e} /pyboard/")
except:
    print("failed")

os.system("exit")
