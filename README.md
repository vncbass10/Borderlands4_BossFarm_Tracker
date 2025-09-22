# Borderlands4_BossFarm_Tracker
A Lightweight overlay with hotkeys to keep track of Boss Farming in Borderlands 4

## Key Binds By Default:
  * **[** &nbsp; : &nbsp; Adds 1 To Dedicated
  * **]** &nbsp; : &nbsp; Adds 1 To World 
  * **=** &nbsp; : &nbsp; Commit to array 
  * **Ctrl+Shift+S** &nbsp; : &nbsp; Saves to output(Same Dir as where you run the script from Named("Data Log.txt"))
  * **Crtl+Shift+L** &nbsp; : &nbsp; Cycle Through Layouts 
  * **Backspace** &nbsp; : &nbsp; Resets Current Run 
  * **Shift+Backspace** &nbsp; : &nbsp; Resets All 
  * **-** &nbsp; : &nbsp; Undo(Max 1) 
  * **Ctrl+Shift+H** &nbsp; : &nbsp; Opens Help 
  * **Ctrl+Shift+C** &nbsp; : &nbsp; Close<br><br>
   _Feel Free to change these within the script in the **Globals** Section_

## Main Features
  * Overlay that displays on top layer of screen(Mixed results with fullscrenn application)
  * Tracks Overall time of session and indiviual runs
  * 3 Different Layouts for the overlay (Verbose, Compact, and Minimal)
  * Has a data set of the bosses and their drops that i have compiled from online sources and a lot of farming
  * Auto populates bosses dedicated drops if bosses name is entered
  * Track Dedicated/ World / and No Drop(Commit a run with no other drops)

## If you want an exe
The Command i recomend is:
```python
pyinstaller --onefile 'Boss Tracker.py' --hide-console minimize-late
```

## Screenshots
### Verbose Overlay
  ![Verbose](/Screenshots/screenshot_verbose.png?raw=true "Verbose Overlay")
### Compact Overlay
  ![Compact](/Screenshots/screenshot_compact.png?raw=true "Compact Overlay")
### Minimal Overlay
  ![Minimal](/Screenshots/screenshot_minimal.png?raw=true "Minimal Overlay")
