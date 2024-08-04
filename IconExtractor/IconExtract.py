import os
import sys
import winreg
import icoextract


def get_user_pictures_path():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            return winreg.QueryValueEx(key, "My Pictures")[0]
    except WindowsError:
        return None


if __name__ == "__main__":
    if len(sys.argv) == 3:
        file_path, file_name = os.path.split(sys.argv[1])
        if sys.argv[2] == "system":
            pictures_path = get_user_pictures_path()
            if pictures_path:
                file_path = os.path.join(pictures_path, "ico")
            else:
                file_path = os.getcwd()

        file_name = file_name[:-4] + ".ico"
        file = os.path.join(file_path, file_name)

        # 确保目标文件夹存在
        os.makedirs(file_path, exist_ok=True)

        icon_extractor = icoextract.IconExtractor(sys.argv[1])
        icon_extractor.export_icon(file)
