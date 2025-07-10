import os
import shutil

def clean_pycache(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            print(f"Deleting: {pycache_path}")
            shutil.rmtree(pycache_path)

if __name__ == "__main__":
    clean_pycache(os.getcwd())
