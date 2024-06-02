import os
import sys
import icoextract

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file_path, file_name = os.path.split(sys.argv[1])
        if sys.argv[2] == "system":
            file_path = r"D:\Document\Pictures\ico"
        file_name = file_name[:-4] + ".ico"
        file = os.path.join(file_path, file_name)
        icon_extractor = icoextract.IconExtractor(sys.argv[1])
        icon_extractor.export_icon(file)
