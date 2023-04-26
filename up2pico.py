import os

folder = "Prototype_keyb/final"

try:
    out = os.popen("rshell ls /pyboard/").read()
    print("______", out, "________________")
    li = out.split()

    elements = []
    for e in li:
        if e[-3:] == ".py" or e[-4:] == ".txt":
            elements.append(e)

    for e in elements:
        os.system(f"rshell rm /pyboard/{e}")

except Exception as e:
    print("failed:", e)

try:
    #os.system("rshell")
    for e in os.listdir(folder):
        os.system(f"rshell cp {folder}/{e} /pyboard/")
except:
    print("failed")

os.system("exit")
