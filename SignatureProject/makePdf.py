from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def makePdf_from_data(text_file,output_pdf):
  with open(text_file,"r",encoding="utf-8") as file:
    text = file.read()

  c = canvas.Canvas(output_pdf,pagesize=letter)
  width,height = letter

  x,y = 50, height - 50
  line_height = 14

  for line in text.split("\n"):
        if y <= 50:  # Create a new page if space runs out
            c.showPage()
            y = height - 50
        
        c.drawString(x, y, line)
        y -= line_height

  c.save()
  print(f"Pdf is saved as {output_pdf}")


makePdf_from_data("extracted_text.txt","my_rulebook.pdf")