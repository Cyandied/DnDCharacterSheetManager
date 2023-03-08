from func import d
import func
from classes import Character
import PySimpleGUI as sg
sg.theme('Dark Grey 13')



layoutStart = [
    [sg.Text('Welcome to the DnD character manager and item/spell encyclopedia!')],
    [sg.Button("Browse characters"),sg.Button("New character")],
    [sg.Button("Browse items"),sg.Button("Browse spells")],
    [sg.Cancel("EXIT")]
]

windowStart = sg.Window('Start', layoutStart)

layoutBase = [
    [sg.Text]
]

layoutCharacter = [
    [sg.Text("Character Name"), sg.Input(default_text=)],
    [sg.TabGroup([[
    sg.Tab("something", layout),
    sg.Tab("something", layout),
    sg.Tab("something", layout),]],
    tab_location="centerTop"),],

]

windowCharacterShow = False

windowListIShow = False
windowListSShow = False

layoutBrowseC = [
]

windowBrowseCShow = False

while True:
    event, vals = windowStart.read()
    if event == sg.WIN_CLOSED or event == 'EXIT':
        break

    if event == "Browse characters":
        windowBrowseC = sg.Window("Browse characters", layoutBrowseC)
        windowBrowseCShow = True
    
    while windowBrowseCShow:
        eventBrowseC, valsBrowseC = windowBrowseC.read()
        if eventBrowseC == sg.WIN_CLOSED or eventBrowseC == 'EXIT':
            break
    
    if event == "New character":
        windowCharacter = sg.Window("Character", layoutCharacter)
        windowCharacterShow = True
    
    while windowCharacterShow:
        eventC, valsC = windowCharacter.read()
        if eventC == sg.WIN_CLOSED or eventC == 'EXIT':
            break

    if event == "Browse items":
        layoutListI = [
        ]
        windowListI = sg.Window("Items", layoutListI)
        windowListIShow = True
    
    while windowListIShow:
        eventI, valsI = windowListI.read()
        if eventI == sg.WIN_CLOSED or eventI == 'EXIT':
            break

    if event == "Browse spells":
        layoutListS = [
        ]
        windowListS = sg.Window("Items", layoutListS)
        windowListSShow = True
    
    while windowListSShow:
        eventS, valsS = windowListS.read()
        if eventS == sg.WIN_CLOSED or eventS == 'EXIT':
            break




windowStart.close()