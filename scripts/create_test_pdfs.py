import os
from io import BytesIO

import httpx
from fpdf import FPDF
from PIL import Image


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Sample PDF with Images and Text", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_image_with_text(self, image_url, text):
        response = httpx.get(image_url)
        image = Image.open(BytesIO(response.content))
        image_path = f"temp_image_{self.page_no()}.png"
        image.save(image_path)

        self.add_page()
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.image(image_path, x=10, y=60, w=190)
        os.remove(image_path)


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Add some images with text
image_urls = [
    "https://via.placeholder.com/300.png",  # Sample image 1
    "https://via.placeholder.com/400.png",  # Sample image 2
]
texts = [
    "This is a sample image with some text. This image is downloaded from the web.",
    "This is another sample image with some more text. It demonstrates how multiple images can be added.",
]

for url, txt in zip(image_urls, texts):
    pdf.add_image_with_text(url, txt)

pdf.output("data/test/pdf/pdf_image_and_text.pdf")
print("PDF created successfully.")
