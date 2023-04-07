import os
import sys
import re
import subprocess

path = sys.argv[1]


def main():
    coverage_files = []

    for file in os.listdir(path):
        reg = re.search("\.coverage-[a-z]{0,15}-[0-9]{0,15}", file)

        if not reg is None:
            coverage_files.append(f"{path}/{reg.string}")

    coverage_files_string = " ".join(coverage_files)

    subprocess.run(f"coverage combine {coverage_files_string}", shell=True)

if __name__ == "__main__":
    main()
