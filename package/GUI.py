import os
import os.path
import PySimpleGUI as sg
import package.GUI_Classes as GUI
import package.CCcommands as OBJcc

sg.ChangeLookAndFeel("DarkGray10")
basicGUIs = GUI.GUI_Base
inputGUI = GUI.GUI_Input

###################################### Main GUI ##################################

def mainGUI():
    scansAllObject = OBJcc.CloudCompare()

    inputProcessing1 = ["Subsample","Compute Normals", "Orthofoto generieren", "CROP 2D", "Recap erstellen", "Do Nothing"]
    inputProcessing2 = ["translate Scans", "SOR", "Compute Curvature", "Remove ScalarFields", "Do Nothing"]
    inputProcessing3 = ["E57","BIN","PLY","Do Nothing"]

    file_list_column = [
            [
            sg.Text("ScanFolder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(initial_folder = "/navvis/data/workingFolder"),
            ],
            [
            sg.Checkbox("Save all Clouds in one project", key="-ALLATONCE-")
            ],
            [sg.Text("Zusätzliche Prozessierungs-optionen",font="Any 12")],
            [
            sg.Text("Cloud operations"),
            sg.Text("     Operations"),
            sg.Text("             Export format")
            ],
            [
            sg.Combo(inputProcessing1, default_value="DoNothing", key="-OPERATION1-"),
            sg.Combo(inputProcessing2, default_value="DoNothing", key="-OPERATION2-"),
            sg.Combo(inputProcessing3, default_value="BIN", key="-EXPORTFORMAT-"),
            ],
            [
            sg.Text("Arbeitsschritte",font="Any 12")
            ],
            [
            sg.Button(("Prozessieren"),enable_events=True, key="-START-"),
            ],
            [sg.Button(("Beenden"), enable_events=True, key="-CANCEL-")
            ],
    ]

    scan_viewer_column = [
        [sg.Text("Scans to process")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Listbox(values=[], enable_events=True, size=(20, 10), key="-SCANLIST-",horizontal_scroll=True),
        sg.Listbox(values=[], enable_events=False, size=(20, 10), key="-SCANSELECT-",horizontal_scroll=True),
        sg.Button(("Clear"), enable_events=True, key="-CLEAR-")],
    ]

    layout = [
        [
        sg.Column(file_list_column,pad=(0,0,0)),
        sg.VSeperator(),
        sg.Column(scan_viewer_column, pad=(0,0,0)),
        ],
    ]
    window = sg.Window("CloudCompare processingHelper by Luki", layout, icon=r"C:/Users/WengerL/OneDrive - Rapp AG/Tools/CC-Direct/V2.1/SF_Icon.ico")

    while True:
        event, values = window.read()
        try:
            scansAllObject.getCloud()
            window["-SCANLIST-"].update(scansAllObject.scansAll)
        except:
            pass
        #scansAllObject.saveAllAtOnce = values["-ALLATONCE-"]
        #scansAllObject.operation1 = values["-OPERATION1-"]
        #scansAllObject.operation2 = values["-OPERATION2-"]
        #scansAllObject.exForm = values["-EXPORTFORMAT-"]
        if event == "-CLEAR-":
            scansAllObject.scanListSelect = []
            window["-SCANSELECT-"].update(scansAllObject.scanListSelect)
        if event == "-SCANLIST-":
            for scan in values["-SCANLIST-"]:
                scansAllObject.scanListSelect.append(scan)
            window["-SCANSELECT-"].update(scansAllObject.scanListSelect)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FOLDER-":
            scansAllObject.scanPath = values["-FOLDER-"]
            scansAllObject.scanListSelect = []
            try:
                scansAllObject.getCloud()
                window["-SCANLIST-"].update(scansAllObject.scansAll)
            except:
                basicGUIs.message("Keine Scans in diesem Verzeichniss gefunden \nPfad überprüfen","Fehler")
                continue

        if event == "-START-":
    
            scansAllObject.saveAllAtOnce = values["-ALLATONCE-"]
            scansAllObject.operation1 = values["-OPERATION1-"]
            scansAllObject.operation2 = values["-OPERATION2-"]
            scansAllObject.exForm = values["-EXPORTFORMAT-"]
        ############ Operation 1    #####################
            if len(scansAllObject.scanListSelect) != 0:
                scansAllObject.scansAll = []
                for scan in scansAllObject.scanListSelect:
                    scansAllObject.scansAll.append(scan)

                scansAllObject.scansAll = scansAllObject.scanListSelect
            if values["-OPERATION1-"] == "Subsample":
                scansAllObject.operation1 = " -SS SPATIAL " + str(inputGUI.input_Number(1,["Subsample resolution"], GUIDescript="Auflösung für spatial subsample in Meter",GUITitle="Subsample")[0])
            
            elif values["-OPERATION1-"] == "Compute Normals":
                scansAllObject.operationsSpecial = "normals"
                scansAllObject.operation1 = " -ORIENT_NORMS_MST " + str(inputGUI.input_Number(1,["Number of Neighbours"], "Neighbour Count")[0])
            elif values["-OPERATION1-"] == "Orthofoto generieren":
                scansAllObject.operationsSpecial = "Orthofoto"
                #scansAllObject.orthofotoExport(resolution= 0.01)
                scansAllObject.operation1 = " -RASTERIZE -GRID_STEP "+ str(inputGUI.input_Number(1,["Subsample resolution"], GUIDescript="Auflösung für Orthofoto in Meter",GUITitle="Auflösung")[0]) +" -VERT_DIR " + str(int(inputGUI.input_Number(1,["Subsample resolution"], GUIDescript="1 für Grundriss, 2 für Schnitt X und 3 für Schnitt Y",GUITitle="Auflösung")[0])) + " -OUTPUT_RASTER_RGB"
                pass
            elif values["-OPERATION1-"] == "CROP 2D":
                scansAllObject.operationsSpecial = "-CROP2D-"
        ############ Operation 2    #####################
            if values["-OPERATION2-"] == "translate Scans":
                scansAllObject.translationMatrix = inputGUI.input_Number(3,["X-Achse         ","Y-Achse         ","Z-Achse      "],GUIDescript="Translate scans on Plane XYZ", GUITitle="Transalate")
                scansAllObject.operation1 = "translate"
                scansAllObject.translate()
            elif values["-OPERATION2-"] == "SOR":
                sorParameters = inputGUI.input_Number(2,["Neighbours            ", "sigma           "], GUIDescript="Statistical outlier removal Filter",GUITitle="SOR")
                scansAllObject.operation2 = " -SOR " + str(int(sorParameters[0])) + " " + str(float(sorParameters[1]))
            elif values["-OPERATION2-"] == "Compute Curvature":
                curvCompVars=curvCompGUI()
                scansAllObject.operation2 = " -CURV " + curvCompVars[0] + " " + str(int(curvCompVars[1]))           
            elif values["-OPERATION2-"] == "Remove ScalarFields":
                scansAllObject.operation2 = " -REMOVE_ALL_SFS"
            if values["-OPERATION1-"] != "Recap erstellen":
                try:
                    scansAllObject.commandLineCreator()
                    scansAllObject.baseDirCC()
                    os.system(scansAllObject.ccCommand)
                    scansAllObject.getCloud()
                except:
                    basicGUIs.message("Der Cloudcompare Befehl konnte nicht  erstellt oder ausgeführt werden","Fehler")
                    continue
            else:
                    layout =[
                    [sg.Text("Recap Einstellungen")],
                    [sg.Checkbox(key="-RECAPCOMBINE-", text="Recap zusammenfassen in 1 Datei")],
                    [sg.Text('Recap name\n falls nicht ausgefüllt, wird der Scanname genommen')],
                    [sg.InputText(key="-RECAPNAME-")],
                    [sg.Button("OK"),sg.Cancel()]
                    ]
                    recapWindow = sg.Window('Rename Recap', layout)
                    valuesRecap = recapWindow.read()
                    recapVar = valuesRecap[1]["-RECAPCOMBINE-"]
                    recapName = valuesRecap[1]["-RECAPNAME-"]
                    recapWindow.close()
                    if len(scansAllObject.scanListSelect) != 0:
                        scansAllObject.scansAll = []
                        for scan in scansAllObject.scanListSelect:
                            scansAllObject.scansAll.append(scan)
                        scansAllObject.scansAll = scansAllObject.scanListSelect
                        scansAllObject.recap(recapVar, recapName)
                        scansAllObject.getCloud()
                    else:
                        scansAllObject.recap(recapVar, recapName)
                        scansAllObject.getCloud()
                    if event == "-CANCEL-":
                        break
        
        
        if event == "-RECAP-":
            layout =[
            [sg.Text("Recap Einstellungen")],
            [sg.Checkbox(key="-RECAPCOMBINE-", text="Recap zusammenfassen in 1 Datei")],
            [sg.Text('Recap name\n falls nicht ausgefüllt, wird der Scanname genommen')],
            [sg.InputText(key="-RECAPNAME-")],
            [sg.Submit(),sg.Cancel()]
            ]
            window = sg.Window('Rename Recap', layout)
            event, values = window.read()
            recapVar = values["-RECAPCOMBINE-"]
            recapName = values["-RECAPNAME-"]
            window.close()
            if len(scansAllObject.scanListSelect) != 0:
                scansAllObject.scansAll = []
                for scan in scansAllObject.scanListSelect:
                    scansAllObject.scansAll.append(scan)
                scansAllObject.scansAll = scansAllObject.scanListSelect
                scansAllObject.recap(recapVar, recapName)
                scansAllObject.getCloud()
            else:
                scansAllObject.recap(recapVar, recapName)
                scansAllObject.getCloud()
        if event == "-CANCEL-":
            break
    window.close()

def curvCompGUI():
    __return = []
    inputCurvType = ["Mean", "Gaussian", "Normal Change Rate"]
    file_list_column = [
            [sg.Text("Kernel Size"), sg.Text("   Type")],
            [sg.InputText(size=(10,10), key="-KERNEL-"), sg.Combo(inputCurvType, default_value="DoNothing", key="-OPERATIONCT-"),],
            [sg.Button(("OK"),enable_events=True, key="-OK-"),],
    ]

    layout = [
        [sg.Column(file_list_column),]
    ]

    window = sg.Window("Compute Curvature", layout, icon=r"C:/Users/WengerL/OneDrive - Rapp AG/Tools/CC-Direct/V2.1/SF_Icon.ico")

    while True:
        event, values = window.read()
        if values["-OPERATIONCT-"] == "Mean":
            __return.append("MEAN")
        elif values["-OPERATIONCT-"] == "Gaussian":
            __return.append("GAUSS")
        elif values["-OPERATIONCT-"] == "Normal Change Rate":
            __return.append("NORMAL_CHANGE")
        __return.append(values["-KERNEL-"])
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            break
        if event == "-OK-":
            window.close()
            return __return