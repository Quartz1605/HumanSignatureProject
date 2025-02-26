import pdfplumber 
from transformers import pipeline
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap



def summary_maker(input_pdf,output_pdf):
  text = ""
  with pdfplumber.open(input_pdf) as pdf:
    for page in pdf.pages:
      text += page.extract_text() + "\n\n"

  
  max_length = 100

  summarizer = pipeline("summarization",model="facebook/bart-large-cnn")
  
  summary = summarizer(text,max_length=max_length,min_length=50,do_sample=False)[0]['summary_text']

  c = canvas.Canvas(output_pdf,pagesize=letter)
  width,height = letter

  x_margin = 50
  y_position = height-50
  line_height = 14
  max_width = width - 2 * x_margin

  wrapped_text = []
  for paragraph in summary.split("\n"):
    wrapped_text.extend(wrap(paragraph, width=90))

  for line in wrapped_text:
    if y_position <= 50:  # If the page is full, create a new page
        c.showPage()
        y_position = height - 50

    c.drawString(x_margin, y_position, line)
    y_position -= line_height



  

  c.save()
  print(f"Pdf is saved as {output_pdf}")


summary_maker("Airbnb Policies.pdf","Policies_summarized.pdf")