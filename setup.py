import os

os.system("clear")

print('1. Termux')
print('2. Linux')

enter = input('Enter Your Enviroment: ').strip()

if enter == "1":
    print("Please Wait We Are Check Requirements.......... ")
    os.system('pkg update -y && pkg upgrade -y')
    os.system('pkg install python -y')
    os.system('pip3 install -r requirements.txt')
else:
    print('Invaild Option Or System Not Detected')

if enter == "2":
    print("Please Wait We Are Check Requirements..........")
    os.system('sudo apt install python3-venv -y')
    os.system('python3 -m venv myvenv')
    with open("activate_venv.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd myvenv\n")
        f.write("source bin/activate\n")
    
    os.system('chmod +x activate_venv.sh')
    os.system("pip3 install -r requirements.txt")
    print("Run 'bash activate_venv.sh' to activate the virtual environment. ")

else:
    print("Invalid Option Or System Not Detected")
