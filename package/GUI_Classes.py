# import libraries
from email import message
import os
import os.path
from tkinter import font
from turtle import position
from typing import Any
import PySimpleGUI as sg



class GUI_Base:
    def message(text="text",title="title"):
        message = [
            [
            sg.Text(text),
            ],
            [sg.Button(("OK"),enable_events=True, key="-OK-"), sg.Button(("Cancel"),enable_events=True, key="-CANCEL-"),
            ],
        ]
            # ----- Full layout -----
        layout = [
            [
                sg.Column(message),
            ]
        ]

        window = sg.Window(title, layout, icon=r"C:/Users/WengerL/OneDrive - Rapp AG/Tools/CC-Direct/V1.41/SF_Icon.ico")

        # Run the Event Loop
        while True:
            event, values = window.read()
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                window.close()
                break
            if event == "-OK-":
                break
            return

        window.close()
    def Confirm(text="text",title="title",confirmation=False):
        message = [
        [
        sg.Text(text),
        ],
        [sg.Button(("Ja"),enable_events=True, key="-YES-"),sg.Button(("Nein"),enable_events=True,key="-NO-"), sg.Button(("Cancel"),enable_events=True, key="-CANCEL-"),
        ],
        ]
            # ----- Full layout -----
        layout = [
            [
            sg.Column(message),
            ]
        ]

        window = sg.Window(title, layout, icon=r"C:/Users/WengerL/OneDrive - Rapp AG/Tools/CC-Direct/V1.41/SF_Icon.ico")

        # Run the Event Loop
        while True:
            event, values = window.read()
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                window.close()
            if event == "-YES-":
                confirmation = True
                window.close()
                return confirmation
            if event == "-NO-":
                confirmation = False
                window.close()
                return confirmation
            return

class GUI_Input(GUI_Base):
    def __init__(self):
        GUI_Base.message()
    columns=3
    def input_Number(columns,columnTitle=["title             " for i in range(columns)],GUIDescript="Description", GUITitle="Title"):
        lstGUI=[]
        GUITitles =[]
        keyCnt =[]
        for i in range(columns):
            GUITitles.append(sg.Text(columnTitle[i]))
            pos = str(i+1)
            keyCnt.append("-C"+pos+"-")
            lstGUI.append(sg.InputText(size=(10,10), key=keyCnt[i]))

        file_list_column = [
        [
        sg.Text(GUIDescript),
        ],
        GUITitles
        ,
        lstGUI
        ,
        [sg.Button(("OK"),enable_events=True, key="-OK-"), sg.Button(("cancel"),enable_events=True, key="-CANCEL-")
        ],
        ]
    # ----- Full layout -----
        layout = [
        [
            sg.Column(file_list_column),
        ]
        ]

        window = sg.Window(GUITitle, layout, icon=r"C:/Users/WengerL/OneDrive - Rapp AG/Tools/CC-Direct/V1.41/SF_Icon.ico")

    # Run the Event Loop
        while True:
            event, values = window.read()
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                window.close()
                return
            if event == "-OK-":
                valueInput=[]
                for key in keyCnt:
                    valueInput.append(values[key])
                    i=0
                    try:
                        for number in valueInput:
                            number = float(number)
                            valueInput[i]=number
                            i += 1
                    except:
                        GUI_Base.message("Nummer falsch \n überprüfe die Eingabe","Fehler")
                window.close()
                return valueInput