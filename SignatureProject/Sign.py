import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Step 1: Find the text position using OCR
def find_text_position(pdf_path, page_num, target_text):
    doc = fitz.open(pdf_path)
    page = doc[page_num]

    # Render the page as an image
    pix = page.get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes("png")))

    # Use Tesseract OCR to extract text and positions
    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # Search for the target text in detected text
    for i, text in enumerate(ocr_data["text"]):
        if target_text.lower() in text.lower():
            x, y, w, h = (
                ocr_data["left"][i],
                ocr_data["top"][i],
                ocr_data["width"][i],
                ocr_data["height"][i],
            )
            return (x, y + h + 10, x + w, y + h + 60)  # Place image **below** the text
    
    return None  # Return None if text is not found

# Step 2: Overlay the image beneath the text
def add_image_beneath_text(pdf_path, image_path, page_num, target_text, output_pdf):
    doc = fitz.open(pdf_path)

    # Find the position below the target text
    bbox = find_text_position(pdf_path, page_num, target_text)
    if not bbox:
        print(f'Text "{target_text}" not found!')
        return

    # Overlay the image at the detected position
    page = doc[page_num]
    rect = fitz.Rect(*bbox)
    page.insert_image(rect, filename=image_path)

    # Save the final PDF
    doc.save(output_pdf)
    doc.close()
    print(f'Image added successfully below "{target_text}" at {bbox}')

# Example Usage
pdf_file = "Doc.pdf"
image_file = "signature.jpg"
output_pdf = "document_with_image.pdf"

# Place image below the given text on page 1
add_image_beneath_text(pdf_file, image_file, page_num=0, target_text="Signature", output_pdf=output_pdf)
