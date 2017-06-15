import keyboard
from pynput.keyboard import Key, Controller
import time
import string
import clipboard
import sys
# appjar klasörü
# sys.path.append("E:\PYLIB")
from appJar import gui

def lines():
    # Dosyadaki satırları döndüren fonksiyon
    file = open("hotkeys.dat", "r")
    lines = file.readlines()
    i = 0
    for line in lines:
        line = line.replace("\n", "")
        lines[i] = line
        i += 1
    return lines


def add_number(line_arr):
    # Satırarın başına sayı ekleyen fonksiyon
    i = 0
    for line in line_arr:
        line = str(i)+" - "+line
        line_arr[i] = line
        i += 1
    return line_arr


def ekle(btn):
    # Dosyaya satır ekleyecek fonksiyon
    key_bind = app.getEntry("new_binding")
    func_name = app.getOptionBox("functions")
    func_val = app.getEntry("value")
    line = key_bind+";"+func_name+";"+func_val+"\n"
    file = open("hotkeys.dat", "a")
    file.write(line)
    file.close()
    app.updateListItems("list", add_number(lines()))
    app.clearAllEntries()


def sil(btn):
    # Dosyadan satır silen fonksiyon
    id = int(app.getEntry("silinecek"))
    file = open("hotkeys.dat", "r")
    old_lines = file.readlines()
    new_lines = []
    i = 0
    for line in old_lines:
        if(i != id):
            new_lines.append(line)
        else:
            print("silindi")
        i += 1
    file.close()
    file = open("hotkeys.dat", "w")
    file.writelines(new_lines)
    file.close()
    app.clearAllEntries()
    app.updateListItems("list", add_number(lines()))



# Global değişkenlerRamazan
string = ""
secilen_harf = ""
userInput = ""

# Uygulamanın tasarım kısmı
app_height, app_witdh = ["400", "350"]

app = gui("Keyboard", app_height+"x"+app_witdh)

app.addListBox("list", add_number(lines()), 0, 0, 3)
app.addOptionBox("functions", ["-Fonksiyon-", "uppercase", "write"], 1, 0, 2)
app.addEntry("new_binding", 2, 0, 3)
app.setEntryDefault("new_binding", "Tuş Kombinasyonunu ")

app.addEntry("value", 1, 2, 1)
app.setEntryDefault("value", "Fonksiyonun Değeri")

app.addButton("ekle", ekle, 3, 0, 3)
app.setButtonWidth("ekle", app_witdh)

app.addEntry("silinecek", 4, 0, 1)
app.setEntryDefault("silinecek", "Silinecek ID")

app.addButton("Sil", sil, 4, 1, 2)
app.setButtonWidth("Sil", int(int(app_witdh)/2))
##########################################################


def write(value):
    #Ekrana verilen değeri yazan fonksiyon
    keyb = Controller()
    clipboard.copy(value)
    print("Yazılacak metin:"+value)
    keyb.press(Key.ctrl)
    keyb.press("v")
    keyb.release(Key.ctrl)
    keyb.release("v")


def uppercase(value):
    # Kopyalanan veriyi büyük harfe çevirip clipboarda atan fonksiyon
    keyb = Controller()
    keyb.press(Key.ctrl)
    keyb.press("c")
    keyb.release(Key.ctrl)
    keyb.release("c")
    text = clipboard.paste()
    text = text.upper()
    clipboard.copy(text)
    print("Uppercase")
    return 0


def checkKeyBinding(userKeys, lines):
    # Tuş Kombinasyonunu kontrol eden fonksiyon
    global string
    for line in lines:
        line_key = line.split(';')[0]
        line_action = line.split(';')[1]
        line_value = line.split(';')[2]
        if(line_key == userKeys):
            string = line_action+" "+line_value
            globals()[line_action](line_value)




def onKeyPressedEvent(e):
    global userInput, string
    if (e.event_type == 'up'):
        userInput = ""
    else:
        if(userInput == ""):
            userInput = userInput + e.name
        else:
            userInput = userInput + "+" + e.name
    string = userInput
    if(len(userInput.split('+')) >= 2):
        app.setEntry("new_binding", string)
        checkKeyBinding(userInput, lines())


keyboard.hook(onKeyPressedEvent)


def checkStop():
    if(app.yesNoBox("Çıkış", "Çıkış Yap?")):
        exit(0)
        return 0


app.setStopFunction(checkStop)
app.go()
# app.registerEvent(guncelle)
# Sürekli yenilenmesi için fonksiyonu register ediyoruz.



































# def onKeyPressetEvent(e):
#     if (e.event_type == 'down'):
#         global string
#         if(string != ""):
#             string = string+"+"+e.name
#         else:
#             string = e.name
#         print(str(e.scan_code)+" "+e.name+" "+e.event_type)
#     else:
#         string = ""

# def onKeyPressetEvent(e):
#     if (e.event_type == 'up'):
#         global string
#         string = ""
#     else:
#         string = ""
#         string = app.getOptionBox("first")+"+"+app.getOptionBox("second")+string+"+"+e.name
