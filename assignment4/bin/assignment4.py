import os
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds

def main():
    # Retrieve environment variable
    asset_name = os.getenv("ASSET")

    print(f"Environment variable ASSET = {asset_name}")

    # Create a new group with the asset name
    asset_group = cmds.group(em=True, name=f"{asset_name}_GRP")
    print(f"Created group: {asset_group}")

    # Create some geometry
    geo = cmds.polySphere(name=f"{asset_name}_geo")[0]
    cmds.parent(geo, asset_group)
    print(f"Created geometry: {geo} and parented it to {asset_group}")

    # Save the scene using the asset name
    current_dir = os.getcwd()  # Get the current directory
    scene_path = os.path.join(current_dir, f"{asset_name}_scene.mb")
    cmds.file(rename=scene_path)
    cmds.file(save=True)
    print(f"Scene saved as: {scene_path}")

if __name__ == "__main__":
    main()