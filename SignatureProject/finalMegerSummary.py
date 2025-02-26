import pdfplumber 
from transformers import pipeline
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
import fitz

pdf_list = ["Airbnb Policies.pdf", "hackStatement.pdf"]

def chunk_text(text, chunk_size=500):
    
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def summary_maker(input_pdf_list, output_pdf):
    merged_pdf = fitz.open()

    # Merge PDFs
    for pdf in input_pdf_list:
        doc = fitz.open(pdf)
        merged_pdf.insert_pdf(doc)

    text = ""

    # Extract text from ALL PDFs
    for pdf_file in input_pdf_list:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:  # Avoid NoneType issues
                    text += extracted_text + "\n\n"

    if not text.strip():
        print("No text extracted from PDFs. Ensure they are not scanned images.")
        return

    # Summarization in Chunks
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = chunk_text(text, chunk_size=500)
    summaries = [summarizer(chunk, max_length=100, min_length=50, do_sample=False)[0]['summary_text'] for chunk in chunks]

    summary = " ".join(summaries)

    # Create summarized PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    x_margin = 50
    y_position = height - 50
    line_height = 14

    wrapped_text = []
    for paragraph in summary.split("\n"):
        wrapped_text.extend(wrap(paragraph, width=90))

    for line in wrapped_text:
        if y_position <= 50:  # New page if space runs out
            c.showPage()
            y_position = height - 50

        c.drawString(x_margin, y_position, line)
        y_position -= line_height

    c.save()
    print(f"PDF saved as {output_pdf}")

summary_maker(pdf_list, "DOne.pdf")

