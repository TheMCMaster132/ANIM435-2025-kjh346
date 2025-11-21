import os
import json
import getpass
from datetime import datetime
import logging
import maya.standalone
maya.standalone.initialize()
import maya.utils
import maya.cmds as cmds

# Logging setup
handler = maya.utils.MayaGuiLogHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)

logger.addHandler(handler)
logger.propagate = False

def export_metadata(metadata, output_path):
    # Writes metadata to a JSON file
    try:
        with open(output_path, "w") as f:
            json.dump(metadata, f, indent=4)
        logger.info(f"Metadata exported to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to write metadata JSON: {e}")

def main():
    logger.info("Starting script...")

    # Retrieve environment variable
    asset_name = os.getenv("ASSET")
    if not asset_name:
        logger.error("ASSET environment variable not set. Exiting.")
        return

    logger.info(f"Environment variable ASSET = {asset_name}")

    # Create a new group with the asset name
    if cmds.objExists(f"{asset_name}_GRP"):
        logger.warning(f"Group {asset_name}_GRP already exists. Using existing one.")
        asset_group = f"{asset_name}_GRP"
    else:
        asset_group = cmds.group(em=True, name=f"{asset_name}_GRP")
        logger.info(f"Created group: {asset_group}")

    # Create some geometry
    geo = cmds.polySphere(name=f"{asset_name}_geo")[0]
    cmds.parent(geo, asset_group)
    logger.info(f"Created geometry: {geo} and parented it to {asset_group}")

    # Save the scene using the asset name
    current_dir = os.getcwd()
    if not os.path.isdir(current_dir):
        logger.warning(f"Working directory {current_dir} is invalid. Maya may save elsewhere.")

    scene_path = os.path.join(current_dir, f"{asset_name}_scene.mb")
    cmds.file(rename=scene_path)
    cmds.file(save=True)
    logger.info(f"Scene saved as: {scene_path}")

    # Export metadata
    metadata = {
        "asset": asset_name,
        "saved_scene": scene_path,
        "user": getpass.getuser(),
        "maya_scene_name": cmds.file(query=True, sceneName=True),
        "export_time": datetime.now().isoformat(),
        "maya_version": cmds.about(version=True),
        "workspace": cmds.workspace(q=True, rd=True),
        "environment_vars": {
            "ASSET": os.getenv("ASSET"),
            "HOME": os.getenv("HOME"),
            "USER": os.getenv("USER"),
        },
        "objects_created": {
            "group": asset_group,
            "geometry": geo
        }
    }

    metadata_path = os.path.join(current_dir, "metadata.json")
    export_metadata(metadata, metadata_path)

    logger.info("Script finished successfully.")

if __name__ == "__main__":
    main()