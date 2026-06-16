import json
import os

def GetPrintFileValue(filePath):
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print("File not found:", filePath)
        return None

    except json.JSONDecodeError:
        print("Invalid JSON format")
        return None

    except Exception as e:
        print(type(e), str(e))
        return None

def CreateOrWriteFile(filePath, content):
    try:
        # Create parent folders if they don't exist
        folder = os.path.dirname(filePath)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(filePath, "x", encoding="utf-8") as file:
            file.write(content)

        print("File created and written successfully")

    except FileExistsError:
        with open(filePath, "a", encoding="utf-8",) as f:
            f.write(content+"\n")
            print("File already existed, content overwritten")

    except Exception as e:
        print("This is finally exception")
        print(type(e), str(e))