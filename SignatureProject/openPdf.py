import fitz

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n\n"

    return text

pdf_path = "Rulebook_CodeRed.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

with open("extracted_text.txt","w",encoding="utf-8") as file :
    file.write(extracted_text)

print("Text extraction complete.Check extracted _text.txt")