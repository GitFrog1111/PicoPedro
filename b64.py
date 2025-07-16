import base64


def encode_image_to_base64_string_and_save(image_path: str, output_txt_file_path: str) -> bool:
    """
    Encodes an image file to a base64 string and saves it to a specified .txt file.

    This function relies on the 'base64' module, which must be imported
    in the environment where this function is called. For example:
    import base64

    Args:
        image_path (str): The path to the source image file (e.g., "image.png").
        output_txt_file_path (str): The path where the .txt file containing the
                                    base64 string will be saved (e.g., "output_b64.txt").

    Returns:
        bool: True if the image was successfully encoded and saved, False otherwise.
    """
    try:
        # Attempt to use the base64 module. This will raise a NameError if 'base64'
        # is not imported in the calling scope.
        # We reference it here indirectly by trying to access an attribute.
        # A direct call like base64.b64encode would be the actual use.
        if not hasattr(base64, 'b64encode'): # type: ignore
            # This check is mostly illustrative; the NameError on actual use is key.
            pass # Fall through to actual usage which will raise NameError if not imported

        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        
        # Encode bytes to base64 bytes, then decode to UTF-8 string
        base64_encoded_bytes = base64.b64encode(image_bytes) # type: ignore
        base64_string = base64_encoded_bytes.decode('utf-8')
        
        with open(output_txt_file_path, "w") as txt_file:
            txt_file.write(base64_string)
            
        return True
            
    except FileNotFoundError:
        # Handle cases where the image_path or output_txt_file_path is invalid
        # or the file cannot be created.
        # print(f"Error: File not found or path issue. Check '{image_path}' and '{output_txt_file_path}'.")
        return False
    except NameError:
        # This error occurs if the 'base64' module is not imported.
        # Raise a more specific error to guide the user.
        raise RuntimeError(
            "The 'base64' module is not imported. Please import it before calling this function."
        )
    except Exception:
        # Catch any other unexpected errors during the process.
        # print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    encode_image_to_base64_string_and_save("imageguide2.jpeg", "output_b642.txt")