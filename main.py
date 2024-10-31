"""
Icon Builder Script.
"""

import os

from PIL import Image
from termcolor import colored


def add_transparent_space(image_path, output_path):
    print(
        colored("PROCESS:", "yellow", attrs=["bold"]),
        colored(f"{image_path}", "dark_grey"),
    )
    try:
        # Load the JPG image
        img = Image.open(image_path).convert("RGBA")

        # Original dimensions
        original_width, original_height = img.size

        # Desired dimensions
        desired_width = 256
        desired_height = 256

        # Create a new image with a transparent background
        new_img = Image.new(
            "RGBA",
            (desired_width, desired_height),
            (0, 0, 0, 0),
        )

        # Calculate the position to center the original image horizontally
        left = (desired_width - original_width) // 2
        top = 0

        # Paste the original image onto the new image
        new_img.paste(img, (left, top))

        # Save the image with added transparent space as ICO
        new_img.save(output_path, format="ICO", sizes=[(256, 256)])
        print(
            colored("SAVE:", "green", attrs=["bold"]),
            colored(f"{output_path}", "dark_grey"),
        )
        print("")
    except Exception as e:
        print(f"ERROR {image_path}: {e}")


def process_images(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(
            colored(
                f"FOLDER CREATED: {output_folder}",
                "greed",
                attrs=["bold"],
            )
        )

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(
                output_folder, os.path.splitext(filename)[0] + ".ico"
            )
            add_transparent_space(input_path, output_path)
        else:
            print(
                colored(
                    f"IGNORE (NOT PNG): {filename}",
                    "red",
                    attrs=["bold"],
                )
            )


def main():
    """
    Main function of the script.
    """
    print(colored("INITIATING TASK...", "yellow", attrs=["bold"]))
    print("")
    input_folder = "D:/Projects/project_automation/icon_builder/input/"
    output_folder = "D:/Projects/project_automation/icon_builder/output/"
    process_images(input_folder, output_folder)
    print(colored("TASK FINISHED: OK", "green", attrs=["bold"]))


if __name__ == "__main__":
    main()
