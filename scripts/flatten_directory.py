import os
import shutil
import sys
import json

def save_state(directory, state_file):
    state = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            state[file_path] = root
    with open(state_file, 'w') as file:
        json.dump(state, file)

def restore_state(state_file):
    with open(state_file, 'r') as file:
        state = json.load(file)
    for file_path, original_location in state.items():
        if os.path.exists(file_path):
            shutil.move(file_path, original_location)

def flatten_directory(directory, levels):
    for root, dirs, files in os.walk(directory, topdown=False):
        depth = root[len(directory):].count(os.sep)
        if depth > levels:
            for file in files:
                file_path = os.path.join(root, file)
                target_path = os.path.join(directory, file)
                shutil.move(file_path, target_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flatten_directory.py <directory> <levels>")
        sys.exit(1)

    directory = sys.argv[1]
    levels = int(sys.argv[2])
    state_file = 'original_state.json'

    save_state(directory, state_file)
    flatten_directory(directory, levels)

    undo = input("Do you want to undo the changes? (yes/no): ")
    if undo.lower() == 'yes':
        restore_state(state_file)
        print("Changes undone.")
    else:
        print("Changes applied.")
