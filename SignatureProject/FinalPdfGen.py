import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap

def get_make_pdf(filepath,output_pdf_name):
  doc = fitz.open(filepath)
  text = ""

  for page in doc:
    text += page.get_text("text") + "\n\n"

  c = canvas.Canvas(output_pdf_name,pagesize=letter)
  width,height = letter

  x_margin = 50
  y_position = height-50
  line_height = 14
  max_width = width - 2 * x_margin

  wrapped_text = []
  for paragraph in text.split("\n"):
    wrapped_text.extend(wrap(paragraph, width=90))

  for line in wrapped_text:
    if y_position <= 50:  # If the page is full, create a new page
        c.showPage()
        y_position = height - 50

    c.drawString(x_margin, y_position, line)
    y_position -= line_height



  

  c.save()
  print(f"Pdf is saved as {output_pdf_name}")

get_make_pdf("Airbnb Policies.pdf","Our_rulebook.pdf")



