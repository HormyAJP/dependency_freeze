#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import tempfile
import yaml

FREEZE_CONFIG = ".dependency_freeze.yaml"
FREEZE_DIR = ".dependency_freeze"

def ensure_dir_exists(directory):
    try:
        os.makedirs(directory)
    except:
        pass

def read_config():
    with open(FREEZE_CONFIG, 'r') as stream:
        return yaml.safe_load(stream)

# find Pods -type f -exec md5sum "{}" + > checksum.list
def write_checksum_file_for_directory(directory, output_filename):
    cmd = ['find', directory, '-type', 'f', '-exec', 'shasum', '{}', '+']
    print(f"Executing: {' '.join(cmd)}")
    output = subprocess.check_output(cmd).decode()
    with open(output_filename, 'w') as stream:
        stream.write(output)
    print(f"Wrote: {output_filename}")


def generate_hash_filename_for_directory(directory, output_directory):
    return os.path.join(output_directory, f"{'_'.join(directory.split('/'))}.checksums")

def file_contents_are_the_same(left, right):
    cmd = ['diff', left, right]
    print(f"Executing: {' '.join(cmd)}")
    output = subprocess.check_output(cmd).decode()
    return len(output) == 0

def generate(output_directory=FREEZE_DIR):
    print("Cleaning freeze directory: {output_directory}")
    shutil.rmtree(output_directory)
    ensure_dir_exists(output_directory)

    config = read_config()
    for directory in config['directories']:
        output_filename = generate_hash_filename_for_directory(directory, output_directory)
        write_checksum_file_for_directory(directory, output_filename)

def check():
    config = read_config()
    tmpdirname = tempfile.mkdtemp(prefix="dependency_freeze_")
    generate(tmpdirname)
    for directory in config['directories']:
        base_filename = generate_hash_filename_for_directory(directory, FREEZE_DIR)
        temp_filename = generate_hash_filename_for_directory(directory, tmpdirname)
        if not file_contents_are_the_same(base_filename, temp_filename):
            raise Exception(f"Hashes for directory {directory} don't match!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate or check hashes for dependencies')
    parser.add_argument('--generate', action='store_true', help='Generate the checksums')

    args = parser.parse_args()
    print(args.generate)
    if args.generate:
        print("Generating hashes")
        generate()
    else:
        print("Checking hashes")
        check()
