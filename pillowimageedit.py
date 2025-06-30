from PIL import Image, ImageEnhance
import os
import random


def apply_mask(base_image_path: str, output_path: str, brightness: float = 1.0, contrast: float = 1.0, color: float = 1.0, sharpness: float = 1.0):
    """
    Applies a mask to a base image, with optional enhancements.
    The mask's alpha channel or luminance determines the transparency of the output.
    Enhancement factors: 1.0 means no change.
    - brightness: A factor of 0.0 gives a black image, 1.0 gives the original image.
    - contrast: A factor of 0.0 gives a solid grey image, 1.0 gives the original image.
    - color: A factor of 0.0 gives a black and white image, 1.0 gives the original image.
    - sharpness: A factor of 0.0 gives a blurred image, 1.0 gives the original image, and 2.0 gives a sharpened image.
    """
    #choose random mask from static/masks
    mask_image_path = random.choice(os.listdir("static/masks"))
    mask_image_path = "static/masks/" + mask_image_path

    # Open base and mask images
    try:
        base_image = Image.open(base_image_path)
        mask_image = Image.open(mask_image_path)
    except IOError as e:
        raise
    
    #choose random rotation from 0, 1, 2, 3
    rotation = random.randint(0, 3)
    #rotate mask image by rotation
    mask_image = mask_image.rotate(rotation * 90)

    # Apply enhancements
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(base_image)
        base_image = enhancer.enhance(brightness)

    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(base_image)
        base_image = enhancer.enhance(contrast)

    if color != 1.0:
        enhancer = ImageEnhance.Color(base_image)
        base_image = enhancer.enhance(color)

    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(base_image)
        base_image = enhancer.enhance(sharpness)

    # Ensure base image is RGBA to support transparency
    if base_image.mode != "RGBA":
        base_image = base_image.convert("RGBA")

    # Get the mask from the alpha channel if it exists, otherwise from luminance
    if 'A' in mask_image.getbands():
        mask = mask_image.getchannel('A')
    else:
        mask = mask_image.convert('L')

    # Ensure mask and base image are the same size
    if base_image.size != mask.size:
        mask = mask.resize(base_image.size, Image.LANCZOS)

    # Apply the mask
    base_image.putalpha(mask)

    # Save the result
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    base_image.save(output_path)

    return base_image

# --- Test Call ---
# Note: This test requires a 'static/masks' directory with at least one mask image.
if os.path.isdir("static/masks") and len(os.listdir("static/masks")) > 0:
    apply_mask(
        base_image_path="static/town.jpeg",
        output_path="static/POI_enhanced.png",
        brightness=1.15,
        contrast=0.95,
        color=1,
        sharpness=0.1
    )
else:
    pass
