import keyboard
import time
import sys
import os
import tkinter as tk
from tkinter import messagebox
from io import StringIO
#^ Good thing made by better programers ^

if getattr(sys, 'frozen', False):   # File path recognition
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    
#Globals{ All globals are here for ease of access
filePath = f"{application_path}\\Data Log.txt" # Path for output file
runarray = [] # Stores data of all runs (format [[0,0,0,0]...])
lastrunarray = [] # Stores Last array for purpose of undo
currentRun = [0,0,0,0] # [Total Runs, Dedicated drop count, World drop count, No Drop count, Run Time]
original_stdout = sys.stdout # Protects stdout default
bossName = "" # Global for name of Boss
overlay_label_string = StringIO() # String IO for output file
layout_setting = 1 # 0 is full display, 1 is compact, 2 is Minimal  
starttime = time.time()  # Start Time of runs
lastruntime = time.time() # End time of last run

addworldkey = ']'  # Keybinds
adddedicatekey = '[' # Keybinds
commitkey = '=' # Keybinds
savekey = 'S' # Keybinds
resetcurrentkey = 'backspace' # Keybinds
resetallkey = 'backspace' # Keybinds
undokey = '-' # Keybinds
layoutkey = 'L' # Keybinds
helpkey = 'H' # Keybinds
closekey = 'C' # Keybinds

BossData = {
    #Fadefields Location
    "Splashzone":
        ["Fadefields","Lead Ballon","Firewerks","Jelly"],
    "Horace":
        ["Fadefields","Aegon's Dream","Pacemaker","Lucky Clover"],
    "Oppressor":
        ["Fadefields","Streamer","Asher's Rise","Blood Analyzer"],
    "Bio-Bulkhead":
        ["Fadefields","Waterfall","Budget Deity","Sho Kunai"],
    "Idolator Sol":
        ["Fadefields","Gormaster","Onlslaught","Golden God", "Dancer", "Bio-Robot","Furnace", "Technomancer"],
    "Primordial Guardian Inceptus":
        ["Fadefields","Husky Friend","Extra Medium","Ravenfire","Elementalist","Filantropo","Avatar"],
    "Sidney Pointylegs":
        ["Fadefields","Swarm","Noisy Cricket","Disc Jockey"],
    "Sludgemaw":
        ["Fadefields","Onion","Kickballer","Birt's Bees"],
    "Voraxis(Quake Thresher)":
        ["Fadefields","Darkbeast","Potato Thrower IV","Buoy"],
    "Foundry Freaks":
        ["Fadefields","Chuck","Bloody Lumberjack","Chaumurky"],
    "Mimicron":
        ["Fadefields","Complex Root","Luty Madlad","UAV"],
    "Core Observer":
        ["Fadefields","Defibrillator","Bully"],
    "Backhive":
        ["Fadefields","Cindershelly","Stop Gap", "Triple Bypass"],

    #Carcadia Burn Location
    "Moon-Maddened Callis":
        ["Carcadia Burn","Ohm i Got","Gamma Void"],
    "Callis, the Ripper Queen":
        ["Carcadia Burn","Queen's Rest","Pandoran Memento","Viking","Esgrimidor","Skeptic","Illusionist"],
    "Primordial Guardian Radix":
        ["Carcadia Burn","Anarchy","Adreniline Pump"],
    "Leader Willem":
        ["Carcadia Burn","Rainbow Vomit"],
    "Fractis":
        ["Carcadia Burn","Protean Cell","Chuck","UAV"],
    "Genone":
        ["Carcadia Burn","Oscar Mike", "Recursive"],
    "Pango and Bango":
        ["Carcadia Burn","Stray","Prince Harming","Phantom Flame"],
    "Rippa Roadbirds":
        ["Carcadia Burn","Wombo Combo","Spinning Blade"],
    "Driller Hole":
        ["Carcadia Burn","Fuse","Katagawa's Revenge", "G.M.R."],
    "Rocken Roller":
        ["Carcadia Burn","San Saba Songbird","AF1000"],
    "Skull Orichid":
        ["Carcadia Burn","Roach", "Oak-Aged Cask"],

    # Terminus Range Location
    "Skyspanner Kratch": 
        ["Terminus Range","Hellfire","Linebacker","Hoarder"],
    "Meathead Riders": 
        ["Terminus Range","Hellwalker","War Paint","Lucian's Flank"],
    "Shadowpelt":
        ["Terminus Range","Vamoose","Sparky Shield","Slippy"],
    "Callous Harbringer of Annihilating Death":
        ["Terminus Range","Hot Slugger","Atling Gun","Kaleidosplode"],
    "Bramblesong":
        ["Terminus Range","Convergence","Disco"],
    "Battle Wagon":
        ["Terminus Range","Compleation","Finnity XXX-L"],
    "Primordial Guardian Origo":
        ["Terminus Range","Kaoson", "Shatterwight", "Buster","*Bottled Lightning*"],
    "The Divisioner":
        ["Terminus Range","Inkling", "Sideshow"],
    "Vile Prototype":
        ["Terminus Range","Rangefinder","Heavyweight","King's Gambit"],
    "Vile Lictor":
        ["Terminus Range","Instigator","Generator","Ruby's Grasp","Super Soldier","Blockbuster","Undead Eye","Blacksmith"],
    

    # Dominion Location
    "Axemaul":
        ["Dominion","Buzz Axe","Bod"],
    "Primordial Guardian Timekeeper":
        ["Dominion","Plasma Coil","Timekeeper's New Shield"],
    "Directive-O":
        ["Dominion","Bonnie and Clyde","Wiskey Foxtrot"],
    "Vile Ted & The Experiments":
        ["Dominion","Goalkeeper","Seventh Sense"]
}

#}

def all_clear():
    global runarray, lastrunarray, currentRun, bossName, starttime, lastruntime
    runarray = []
    lastrunarray = []
    currentRun = [0,0,0,0]
    bossName = ""
    starttime = time.time()
    lastruntime = time.time()

def update_label():  # Updates overlay label
    global root,label,overlay_label_string
    printString(get_RunData(),overlay_label_string,layout_setting)
    label.config(text=overlay_label_string.getvalue())
    root.update()
    overlay_label_string.truncate(0)
    overlay_label_string.seek(0)
    root.after(100, update_label)

def get_RunData():   #pars data from array returns [Total Runs, Dedicated drop count, World drop count, No Drop count]
    dedicate = 0
    world = 0
    nulldrop = 0
    if len(runarray) > 0:
        for itm in runarray:
            dedicate += itm[0]
            world += itm[1]
            nulldrop += itm[2]
        return len(runarray),dedicate, world, nulldrop
    else:
        return 0,0,0,0

def get_curruntime():   # Gets time of current run
    tmpmin = int((time.time() - lastruntime)/60)
    tmpsec = int((time.time() - lastruntime)%60)
    return f"m:{tmpmin%60} s:{tmpsec}"

def get_runtime():   # Gets time of total runs
    tmpmin = int((time.time() - starttime)/60)
    tmpsec = int((time.time() - starttime)%60)
    return f"m:{tmpmin%60} s:{tmpsec}"

def printString(data, fileobject=original_stdout, layout = 0):   # Convert data to readable formats and sets syntax for output file
    global bossName
    sys.stdout = fileobject
    if fileobject == original_stdout or fileobject == overlay_label_string: 
        os.system("cls")
    else:
        print("\n")
    if layout == 0:     
        print("All Data         | Boss: ",bossName)
        if bossName in BossData:
            print("Location:        |",BossData[bossName][0])
            print("Dedicated Drops: |",BossData[bossName][1:])
                
        print("---------------------------------")
        print("Runs:            |",data[0])
        print("Dedicated Drops: |",data[1])
        print("World Drops:     |",data[2])
        print("No Drops:        |",data[3]) 
        print("Time Spent:      |",get_runtime())
        print("---------------------------------")
    if layout == 1:
        if data[0]<10:print("Total Runs: ",data[0],"  | Boss: ",bossName)
        if data[0]>9 and data[0]<100:print("Total Runs: ",data[0],"      | Boss: ",bossName)
        if data[0]>99 and data[0]<1000:print("Total Runs: ",data[0],"     | Boss: ",bossName)
    
    if fileobject != overlay_label_string and fileobject != original_stdout:
        print("All Runs")
        print("---------------------------------")
        print("  Run  |  Dedicated  |  World  |  No Drop  | Run Time  ")
        
        for i in range(len(runarray)):
            if i <10 : print("  ",i,"  |     ",runarray[i][0],"     |    ",runarray[i][1],"  |    ",runarray[i][2],"    | ",runarray[i][3])
            if i <100 and i >9: print(" ",i,"  |     ",runarray[i][0],"     |    ",runarray[i][1],"  |    ",runarray[i][2],"    | ",runarray[i][3])
            if i <1000 and i >99: print(i,"  |     ",runarray[i][0],"     |    ",runarray[i][1],"  |    ",runarray[i][2],"    | ",runarray[i][3])
        print("---------------------------------")
        print("Raw Data (Dedicated, World, No Drop, Run Time)")
        print("---------------------------------")
        print(bossName,"|",runarray)

        sys.stdout = original_stdout
    
    else:
        if layout_setting < 2:
            print("Current Data")
            print("---------------------------------")
            print("Dedicated Drops: |",currentRun[0])
            print("World Drops:     |",currentRun[1])
            print("---------------------------------")

        if layout_setting == 2:
            print(f"Runs: {data[0]}| D: {currentRun[0]} W: {currentRun[1]}| T:{get_runtime()}")


        sys.stdout = original_stdout

def get_input_text(): # Gets text from input box and sets Boss Name
    global bossName
    """Retrieves the text from the Entry widget and displays it in a message box."""
    bossName = entry_field.get()
    for i in (BossData):
            if bossName.lower() in i.lower():
                bossName = i
                break
    root1.destroy()

def on_key_event(event):  # key even handler
        global currentRun,runarray,lastrunarray,lastruntime,layout_setting, addworldkey, adddedicatekey, commitkey, savekey, resetcurrentkey, resetallkey, undokey, layoutkey, helpkey, closekey
        #print(f"Key: {event.name} Event Type: {event.event_type}")
        if event.name == adddedicatekey:currentRun[0] += 1
        if event.name == addworldkey:currentRun[1] += 1
        if event.name == undokey:runarray = lastrunarray.copy()
        if event.name == resetcurrentkey:
            if keyboard.is_pressed('shift'):
                all_clear()
                build_inputBox()
            else:
                currentRun = [0,0,0,0]

        if event.name == layoutkey:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
                match layout_setting:
                    case 0:
                        layout_setting = 1
                    case 1:
                        layout_setting = 2
                    case 2:
                        layout_setting = 0
        if event.name == commitkey:
            lastrunarray = runarray.copy()
            if currentRun == [0,0,0,0]:
                runarray.append([0,0,1,get_curruntime()])
            else:
                currentRun[3] = get_curruntime()
                runarray.append(currentRun)
            currentRun = [0,0,0,0]
            lastruntime = time.time()
        if event.name == savekey:
            if keyboard.is_pressed('ctrl'):
                with open(filePath, "a") as fileobject:
                    printString(get_RunData(),fileobject,0)
                all_clear()
                build_inputBox()
        if event.name == helpkey:
            if keyboard.is_pressed('ctrl'):
                messagebox.showinfo("Help",f"{adddedicatekey} : Adds 1 To Dedicated \n{addworldkey} : Adds 1 To World \n{commitkey} : Commit to array \n Ctrl+Shift+{savekey} : Saves to output \nCrtl+Shift+{layoutkey} : Cycle Through Layouts \n{resetcurrentkey} : Resets Current Run \nShift+{resetallkey} : Resets All \n{undokey} : Undo(Max 1) \nCtrl+Shift+{helpkey} : Opens Help \nCtrl+Shift+{closekey} : Close \n")
        if event.name == closekey:
            if keyboard.is_pressed('ctrl'):
                root.destroy()
                #exit(0)
     

def build_overlay():   # Builds overlay
    global root
    global label
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost",True)
    root.wm_attributes("-transparentcolor","grey")
    label = tk.Label(root, text="", bg="grey", fg="white",justify="left",anchor="w", font=("Courier New", 16, "bold"))
    label.pack()
    root.geometry("+10+10")
    root.update()
    root.after(0,build_inputBox)
    root.after(100,update_label)

    try:
        root.mainloop()
    except SystemExit as e:
        print("Exiting with status: ", e.code)
    finally: 
        print("Exiting Draw Loop.")
        print("Unhooking all keyboard events and exiting.")
        keyboard.unhook_all()  # Remove all hooks
        print("Exited gracefully.")

def build_inputBox():  # Input Dialoge to avoid console
    global root1, entry_field
    root1 = tk.Toplevel(root)
    ws = root1.winfo_screenwidth()
    hs = root1.winfo_screenheight()
    x = (ws/2) - 150
    y = (hs/2) - 75

    root1.title("Bosses Name")
    root1.geometry('%dx%d+%d+%d' % (300,150,x,y))
    input_label = tk.Label(root1,text="Bosses Name: ")
    input_label.pack(pady=10)
    entry_field = tk.Entry(root1, width=30)
    entry_field.pack(pady=5)
    submit_button = tk.Button(root1, text="Submit",command=get_input_text)
    submit_button.pack(pady=5)
    cancel_button = tk.Button(root1, text="Stop", command=root.destroy)
    cancel_button.pack(pady=5)
    entry_field.focus_set()
    root1.bind('<Return>', lambda event=None: submit_button.invoke())
    root1.mainloop()


keyboard.on_release(on_key_event)  # Defines handler for keyboard input
build_overlay()  # Runs last to avoid stalls