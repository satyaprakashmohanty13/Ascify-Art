
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math
import os
from io import BytesIO

st.set_page_config(layout="wide", page_title="Ascify Art", page_icon="🖼️")

st.title("Ascify Art")

def get_char(input_int, char_array):
    interval = len(char_array) / 256
    return char_array[math.floor(input_int * interval)]

def operation(image, chars, scale_factor, one_char_width, one_char_height, background_color, new_r, new_g, new_b, auto_colors, saturation, brightness):
    char_array = list(chars)

    im = image.convert('RGB')

    fnt = ImageFont.load_default() # Using default font for simplicity in Streamlit

    width, height = im.size
    im = im.resize((int(scale_factor * width), int(scale_factor * height * (one_char_width / one_char_height))), Image.Resampling.NEAREST)
    width, height = im.size
    pix = im.load()
    output_image = Image.new('RGB', (one_char_width * width, one_char_height * height), color=background_color)
    d = ImageDraw.Draw(output_image)

    ascii_string = ""
    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]

            if not auto_colors:
                if r >= new_r: r = new_r
                if g >= new_g: g = new_g
                if b >= new_b: b = new_b

            h = int(r / 3 + g / 3 + b / 3)
            pix[j, i] = (h, h, h)
            d.text((j * one_char_width, i * one_char_height), get_char(h, char_array), font=fnt, fill=(r, g, b))
            ascii_string += str(get_char(h, char_array))
        ascii_string += "\n"

    output_image = ImageEnhance.Color(output_image).enhance(saturation)
    output_image = ImageEnhance.Brightness(output_image).enhance(brightness)

    return output_image, ascii_string

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "bmp", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption='Original Image', use_column_width=True)

    with col2:
        st.subheader("Settings")

        chars = st.text_area("Characters", "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

        scale_factor = st.slider("Scale Factor", 0.01, 0.2, 0.09)
        one_char_width = st.slider("Scale Width", 1, 30, 10)
        one_char_height = st.slider("Scale Height", 1, 30, 18)

        background_color = st.color_picker("Background Color", "#000000")

        auto_colors = st.checkbox("Automatic Colors", True)

        if not auto_colors:
            new_r = st.slider("R", 0, 255, 255)
            new_g = st.slider("G", 0, 255, 255)
            new_b = st.slider("B", 0, 255, 255)
        else:
            new_r, new_g, new_b = 255, 255, 255

        saturation = st.slider("Saturation", 0.0, 10.0, 1.0)
        brightness = st.slider("Brightness", 0.0, 15.0, 1.0)

        if st.button("Generate"):
            output_image, ascii_string = operation(image, chars, scale_factor, one_char_width, one_char_height, background_color, new_r, new_g, new_b, auto_colors, saturation, brightness)

            st.image(output_image, caption='Ascified Image', use_column_width=True)

            st.text_area("ASCII String", ascii_string, height=300)

            # Create a download button for the image
            from io import BytesIO
            buf = BytesIO()
            output_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name="ascified_image.png",
                mime="image/png"
            )

            # Create a download button for the text
            st.download_button(
                label="Download ASCII Text",
                data=ascii_string,
                file_name="ascii_art.txt",
                mime="text/plain"
            )
