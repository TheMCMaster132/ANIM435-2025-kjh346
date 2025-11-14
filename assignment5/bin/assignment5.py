import os
import logging
import maya.standalone
maya.standalone.initialize()
import maya.utils
import maya.cmds as cmds

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"

handler = maya.utils.MayaGuiLogHandler()
handler.setFormatter(logging.Formatter(FORMAT))
handler.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(handler)

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

    logger.info("Script finished successfully.")

if __name__ == "__main__":
    main()