Tool to handle, manipulate and modify [i3](http://i3wm.org/) workspaces.

Copyright 2017 Johannes Lange


## Dependencies
- [i3ipc](http://i3ipc-python.readthedocs.io/)
- [rofi](https://davedavenport.github.io/rofi/)


## Installation
- Clone the repository or download the `i3-ws-tool.py` script.
- Put either `i3-ws-tool.py` or a link to the file in a location contained in your `PATH`.

## Usage
```
usage: i3-ws-tool.py [-h] [ACTION]

Tool to handle, manipulate and modify i3 workspaces.

positional arguments:
  ACTION      Choose one of these actions:
              - menu: Show a menu and choose an action
              - switch: Switch to a workspace chosen from a menu or a new one
              - next-empty: Focus the next empty, numbered  workspace
              - move: Move container to a workspace chosen from a menu or a new one
              - move-next-empty: Move the focused container to the next empty, numbered  workspace
              - rename: Rename the focused workspace
              - clear-output: Move all workspaces from the active output to a different one

options:
  -h, --help  show this help message and exit
```

### i3 Keybindings
You can add keybindings in your i3 configuration, e.g.
```
# call the workspace tool menu
bindsym $mod+F8 exec "i3-ws-tool.py"
# switch to the next empty, numbered workspace
bindsym $mod+n exec "i3-ws-tool.py next-empty"
```
