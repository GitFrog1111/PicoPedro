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

    # Apply the mask (TURNED OFF FOR NOW)
    #base_image.putalpha(mask)

    # Save the result
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    base_image.save(output_path)

    return base_image

def apply_dropshadow(poi_image_path, output_path, shadow_path="static/POIDropShadow.png"):
    """
    Layers the POI image on top of the drop shadow image and saves the result.

    Args:
        poi_image_path (str): Path to the POI image (should support transparency).
        output_path (str): Path to save the composited image.
        shadow_path (str): Path to the drop shadow image. Defaults to "static/POIDropShadow.png".
    """
    from PIL import Image
    import os

    # Open the drop shadow image
    shadow = Image.open(shadow_path).convert("RGBA")
    # Open the POI image
    poi = Image.open(poi_image_path).convert("RGBA")

    # Optionally, resize POI to fit within the shadow if needed
    # Here, we center the POI on the shadow, scaling if it's larger
    shadow_w, shadow_h = shadow.size
    poi_w, poi_h = poi.size

    # If POI is larger than shadow, scale it down to fit
    scale = min(shadow_w / poi_w, shadow_h / poi_h, 1.0)
    if scale < 1.0:
        new_size = (int(poi_w * scale), int(poi_h * scale))
        poi = poi.resize(new_size, Image.LANCZOS)
        poi_w, poi_h = poi.size

    # Center the POI on the shadow
    offset_x = (shadow_w - poi_w) // 2
    offset_y = (shadow_h - poi_h) // 2

    # Composite the images
    composite = shadow.copy()
    composite.alpha_composite(poi, (offset_x, offset_y))

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    composite.save(output_path)
    return composite

def apply_multiply_layer(poi_image_path, multiply_image_path, output_path):
    """
    Layers a multiply image over the POI image using the 'multiply' blend mode and saves the result.

    Args:
        poi_image_path (str): Path to the POI image.
        multiply_image_path (str): Path to the image to be multiplied over the POI image.
        output_path (str): Path to save the composited image.
    """
    from PIL import Image, ImageChops
    import os

    # Open the POI image and multiply image as RGBA
    poi = Image.open(poi_image_path).convert("RGBA")
    multiply_img = Image.open(multiply_image_path).convert("RGBA")

    # Resize multiply image to match POI image size if needed
    if multiply_img.size != poi.size:
        multiply_img = multiply_img.resize(poi.size, Image.LANCZOS)

    # Perform multiply blend mode
    # ImageChops.multiply only works on "RGB", so we need to handle alpha
    poi_rgb = poi.convert("RGB")
    multiply_rgb = multiply_img.convert("RGB")
    multiplied_rgb = ImageChops.add(poi_rgb, multiply_rgb)

    # Handle alpha: use POI's alpha channel
    alpha = poi.getchannel("A")
    result = multiplied_rgb.copy()
    result.putalpha(alpha)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    result.save(output_path)
    return result



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
