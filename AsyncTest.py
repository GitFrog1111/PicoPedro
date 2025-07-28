import streamlit as st
import asyncio
import fal_client
import os

st.set_page_config(layout="wide")

st.title("Concurrent SDXL Image Generation")

os.environ['FAL_KEY'] = st.secrets['falAi']['FAL_KEY']


async def generate_image(prompt: str, col):
    """Submits a prompt to fal-ai/fast-sdxl and returns the image URL."""
    with col:
        st.write(f"Requesting: '{prompt}'")
        try:
            handler = await fal_client.submit_async(
                "fal-ai/fast-sdxl",
                arguments={
                    "prompt": prompt,
                },
            )
            result = await handler.get()
            image_url = result["images"][0]["url"]
            st.write(f"✅ Received: '{prompt}'")
            return image_url
        except Exception as e:
            st.error(f"Error for '{prompt}': {e}")
            return None

async def generate_all_images(cols):
    """Generates three images concurrently."""
    prompts = [
        "A cyberpunk cityscape at night, with flying cars and neon signs",
        "A tranquil Japanese garden with a koi pond and cherry blossoms",
        "An epic fantasy battle with dragons, knights, and wizards",
    ]
    
    tasks = [generate_image(prompt, col) for prompt, col in zip(prompts, cols)]
    
    # asyncio.gather runs all tasks concurrently
    image_urls = await asyncio.gather(*tasks)
    return image_urls

# --- Streamlit UI ---

st.info("Click the button below to generate three images in parallel using Fal AI.")

if st.button("Generate Images", type="primary"):
    with st.spinner("Generating images... this might take a minute."):
        cols = st.columns(3)
        
        # Get or create a new asyncio event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Run the async function in the event loop
        image_urls = loop.run_until_complete(generate_all_images(cols))

    st.success("All images generated!")
    
    # Filter out any Nones from failed requests
    valid_urls = [url for url in image_urls if url]
    
    if valid_urls:
        st.subheader("Results")
        # Display images in the same columns
        for col, url in zip(cols, valid_urls):
            with col:
                st.image(url, use_container_width=True)
