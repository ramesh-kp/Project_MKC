"""
from pathlib import Path 
"""
import os
import shutil
from git import Repo
from pathlib import Path

path = "/home/pimkc/Desktop/Wiras"
repo_dir = "/home/pimkc/Desktop/Wiras/Code"
code_dir = "/home/pimkc/Desktop/Wiras/Code"
username = "ramesh-kp"
password = "ramesh6859"
remote = f"http://{username}:{password}@github.com/ramesh-kp/MKC_Device_Code.git"


if __name__ == "__main__":

    choice = input("Do you want the OTA update......")
    if choice == 'Y' or 'y':
        
        print("Starting the OTA update")
        os.chdir(path)
        
        print("Deleting the previous running folder")
        shutil.rmtree(repo_dir)
        print("Deleted '%s' directory successfully.............." % repo_dir)

        print("Cloning from git")
        Repo.clone_from(remote, repo_dir)
        print("Cloned the '%s' code from git....................." % Path(remote).name[:-4])
        
        os.chdir(code_dir)
        os.system("gnome-terminal -- bash -c 'python3 Main_Code.py; exec bash'")
        
    else:
        print("nope")

