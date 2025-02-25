from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap

def create_fixed_pdf(text_file, output_pdf):
    # Read the extracted text file
    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Initialize PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    x_margin = 50  # Left margin
    y_position = height - 50  # Start from the top of the page
    line_height = 14  # Space between lines
    max_width = width - 2 * x_margin  # Maximum width for text

    # Split text into lines with proper wrapping
    wrapped_text = []
    for paragraph in text.split("\n"):
        wrapped_text.extend(wrap(paragraph, width=90))  # Wrap text to fit

    # Write text to PDF
    for line in wrapped_text:
        if y_position <= 50:  # If the page is full, create a new page
            c.showPage()
            y_position = height - 50

        c.drawString(x_margin, y_position, line)
        y_position -= line_height  # Move to the next line

    # Save the fixed PDF
    c.save()
    print(f"Fixed PDF saved as {output_pdf}")

# Example usage
create_fixed_pdf("extracted_text.txt", "fixed_layout.pdf")
