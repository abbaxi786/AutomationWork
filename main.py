from fileOps.create_files import GetPrintFileValue
from configParser.config_parser import ParserValueConvergence
import os

messages = GetPrintFileValue('library/prints.json')
commands = messages["commands"]

execution = None   # ✅ always define globally


def CommandExe():

    global execution

    while (flow := input("Enter command: ").lower()) != "exit":

        # ================= START =================
        if flow == "start":

            try:
                print("Select operations:")

                check1 = input("File Creation (y/n): ")
                check2 = input("Shell (y/n): ")
                check3 = input("Email (y/n): ")

                print(commands["start"])

                path = input("Config path (enter for default): ").strip()

                if not path or not os.path.exists(path):
                    path = "config/config.json"

                execution = ParserValueConvergence(path)

                if check1.lower() == "y":
                    execution.CreateFile()

                if check2.lower() == "y":
                    execution.RunShell()

                if check3.lower() == "y":
                    execution.RunEmail()

            except Exception as e:
                print("ERROR:", e)

                if execution:
                    execution.StopAll()
                    execution = None

        elif flow == "stop":

            if execution:
                execution.StopAll()
                execution = None
                CommandExe()
                print("System stopped")
            else:
                print("No running execution")

        # ================= RESTART =================
        elif flow == "restart":

            if execution:
                execution.StopAll()
                execution = None

            print("System restarting...")

        # ================= EXIT =================
        elif flow == "exit":

            if execution:
                execution.StopAll()

            print("Exiting system...")
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    CommandExe()