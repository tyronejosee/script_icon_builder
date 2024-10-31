"""
Icon Builder Script.
"""

import os
from PIL import Image
from termcolor import colored

# Constants
SERIES_SIZE = (182, 256)
MOVIES_SIZE = (165, 256)
DESIRED_WIDTH = 256
DESIRED_HEIGHT = 256
INPUT_FOLDER = os.getenv(
    "INPUT_FOLDER",
    "D:/Projects/script_icon_builder/input/",
)
TEMP_FOLDER = os.getenv(
    "TEMP_FOLDER",
    "D:/Projects/script_icon_builder/temp/",
)
OUTPUT_FOLDER = os.getenv(
    "OUTPUT_FOLDER",
    "D:/Projects/script_icon_builder/output/",
)
SUPPORTED_FORMATS = [".jpg", ".jpeg"]


def resize_image(image_path, output_path, size):
    """
    Resizes a JPG image to the specified dimensions and saves it as PNG.

    Args:
        image_path (str): Path to the input JPG image.
        output_path (str): Path to save the resized PNG image.
        size (tuple): Desired size as (width, height).
    """
    print(
        colored("RESIZING:", "cyan", attrs=["bold"]),
        colored(f"{image_path}", "dark_grey"),
    )

    try:
        img = Image.open(image_path).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path, format="PNG")
        print(
            colored("SAVE RESIZED:", "green", attrs=["bold"]),
            colored(f"{output_path}", "dark_grey"),
        )
    except Exception as e:
        print(colored(f"ERROR resizing {image_path}: {e}", "red"))


def add_transparent_space(image_path, output_path):
    """
    Adds transparent space to an image and saves it in ICO format.

    Args:
        image_path (str): Path to the input PNG image.
        output_path (str): Path to save the output ICO file.
    """
    print(
        colored("PROCESS:", "yellow", attrs=["bold"]),
        colored(f"{image_path}", "dark_grey"),
    )

    try:
        img = Image.open(image_path).convert("RGBA")
        original_width, original_height = img.size

        # Create a new image with a transparent background
        new_img = Image.new(
            "RGBA",
            (DESIRED_WIDTH, DESIRED_HEIGHT),
            (0, 0, 0, 0),
        )

        # Calculate position to center the original image
        left = (DESIRED_WIDTH - original_width) // 2
        top = (DESIRED_HEIGHT - original_height) // 2  # Centers vertically

        # Paste the original image onto the new image
        new_img.paste(img, (left, top))

        # Save the image with added transparent space as ICO
        new_img.save(output_path, format="ICO", sizes=[(256, 256)])
        print(
            colored("SAVE:", "green", attrs=["bold"]),
            colored(f"{output_path}", "dark_grey"),
        )
    except FileNotFoundError:
        print(colored(f"ERROR: File not found - {image_path}", "red"))
    except Exception as e:
        print(colored(f"ERROR: Could not process {image_path}: {e}", "red"))


def ensure_folder_exists(folder_path):
    """
    Ensures the specified folder exists; creates it if it does not.

    Args:
        folder_path (str): Path of the folder to check/create.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(
            colored(f"FOLDER CREATED: {folder_path}", "green", attrs=["bold"]),
        )


def is_supported_image(filename):
    """
    Checks if a file has a supported image extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if file is supported, otherwise False.
    """
    return any(filename.lower().endswith(ext) for ext in SUPPORTED_FORMATS)


def process_images(input_folder, temp_folder, output_folder, size):
    """
    Processes each JPG image in the input folder, resizing and converting to PNG.

    Args:
        input_folder (str): Path to the input folder.
        temp_folder (str): Path to the temporary folder for resized PNGs.
        output_folder (str): Path to the output folder for ICO files.
        size (tuple): Desired size for resizing (width, height).
    """
    ensure_folder_exists(temp_folder)
    ensure_folder_exists(output_folder)

    for filename in os.listdir(input_folder):
        if is_supported_image(filename):
            input_path = os.path.join(input_folder, filename)
            temp_path = os.path.join(
                temp_folder, os.path.splitext(filename)[0] + ".png"
            )
            resize_image(input_path, temp_path, size)
            output_path = os.path.join(
                output_folder, os.path.splitext(filename)[0] + ".ico"
            )
            add_transparent_space(temp_path, output_path)
        else:
            print(colored(f"IGNORE (NOT SUPPORTED): {filename}", "red", attrs=["bold"]))


def main():
    """
    Main function of the script.
    """
    print(colored("INITIATING TASK...", "yellow", attrs=["bold"]))

    # Prompt user for resizing version choice
    version_choice = input("Choose version - Series (1) or Movies (2): ")
    if version_choice == "1":
        chosen_size = SERIES_SIZE
        print(colored("Selected Series Version", "blue", attrs=["bold"]))
    elif version_choice == "2":
        chosen_size = MOVIES_SIZE
        print(colored("Selected Movies Version", "blue", attrs=["bold"]))
    else:
        print(colored("Invalid choice. Exiting.", "red"))
        return

    # Process images based on selected version
    process_images(INPUT_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER, chosen_size)
    print(colored("TASK FINISHED: OK", "green", attrs=["bold"]))


if __name__ == "__main__":
    main()
