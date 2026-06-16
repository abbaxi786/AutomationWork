import json

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
        with open(filePath, "x", encoding="utf-8") as file:
            file.write(content)
        print("File created and written successfully")
    except FileExistsError:
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(content)
        print("File already existed, content overwritten")
    except Exception as e:
        print(type(e), str(e))