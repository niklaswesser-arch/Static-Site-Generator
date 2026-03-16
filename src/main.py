import os
import shutil

def copy_static_to_public(src="static", dest="public"):
    if os.path.exists(dest):
        print(f"Deleting {dest} directoy...")
        shutil.rmtree(dest)
    
    print(f"Creating {dest} directory...")
    os.mkdir(dest)

    copy_directory_contents(src,dest)

def copy_directory_contents(src, dest):
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_contents(src_path, dest_path)


def main():
    copy_static_to_public()
    print("\nStatic files copied successfully!")



if __name__ == "__main__":
     main()
    