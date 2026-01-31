from PIL import Image
import os

def flip_image(input_path, output_path, mode="horizontal", scale=0.5):
    try:
        img = Image.open(input_path)

        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if mode.lower() == "horizontal":
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif mode.lower() == "vertical":
            flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif mode.lower() == "both":
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
        else:
            raise ValueError("Invalid mode")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        flipped_img.save(output_path)

        print(f"Image enregistrée : {output_path}")

    except Exception as e:
        print("Erreur :", e)


if __name__ == "__main__":
    input_file = "images/v2.gif"
    output_file = "images/v2_small2.gif"

    flip_image(input_file, output_file, mode="horizontal", scale=0.4)