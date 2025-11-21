# Environment Variable Maya Tool

## Description
This tool demonstrates how to access and use **environment variables in Maya** using Python and `maya.cmds`. It runs in **standalone mode** (via `mayapy`) and performs a series of automated tasks based on the environment variable `ASSET`.
It also uses logging to give feedback to the user so that they know exactly what happens in the script and if there are any errors, as well as exports a **metadata JSON file** that records useful information.

The script uses the `ASSET` variable to:
1. **Create a Group** — named after the asset  
2. **Create a Polygon Sphere** — named after the asset and parented under the group  
3. **Save the Maya Scene** —  with the asset name in the current Git Bash directory  

## How to Run
1. **Set the environment variable** in Git Bash:
   ```bash
   export ASSET=thingy
2. **Confirm it's set**:
   ```bash
   echo $ASSET
3. **Navigate to your project directory** (ie.):
   ```bash
   cd /c/Users/Kyle/Desktop/anim-435-2025-kjh346/ANIM-435-2025-kjh/assignment6/bin
4. **Run the script using Maya Standalone**:
   ```bash
   mayapy assignment6.py