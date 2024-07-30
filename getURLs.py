from pywinauto import Application, findwindows
import keyboard


def saveCurrent(curr_set):
    with open("saveFile.txt", "w") as file:
        for element in curr_set:
            file.write(str(element) + "\n")


def readInSaved():
    file1 = open("saveFile.txt", "r")
    lines = file1.readlines()
    valSet = set()
    for l in lines:
        formatted_url = l.strip()
        if len(formatted_url) == 0:
            continue

        if formatted_url not in valSet:
            valSet.add(formatted_url)

    return valSet


urlSet = readInSaved()

# Find all Chrome windows
chrome_windows = findwindows.find_elements(title_re=".*Chrome.*")

# flaw, doesn't get http://, http://, or www.
# I add https:// automatically

# Note - when pasting in url to list manually, sometimes it has www., remove it
pause = True

print(urlSet)
print("----------------------STARTING----------------------")
print("------------------UN-PAUSE_TO_START-----------------")
while True:
    if not pause:
        try:
            window = chrome_windows[0]
            chrome_window_handle = window.handle
            chrome_app = Application(backend="uia").connect(handle=chrome_window_handle)
            element_name = "Address and search bar"
            dlg = chrome_app.top_window()
            url = dlg.child_window(title=element_name).get_value()

            formatted_url = "https://" + url.strip()
            print(formatted_url)
            if formatted_url not in urlSet:
                print(formatted_url + "\n")
                urlSet.add(formatted_url)
        except Exception as e:
            print("Error", e)
            saveCurrent(urlSet)

    if keyboard.read_key() == "q":
        print("----------------------QUITTING----------------------")
        break
    if keyboard.read_key() == "s":
        print("-----------------------SAVING-----------------------")
        saveCurrent(urlSet)
    if keyboard.read_key() == "p":
        if pause:
            print("---------------------UN-PAUSING---------------------")
        else:
            print("-----------------------PAUSING----------------------")

        pause = not pause

print("------------------------SAVING----------------------")

saveCurrent(urlSet)
