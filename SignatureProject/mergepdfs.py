import fitz

def merge_pdfs(pdf_list,output_name):
  merged_pdf = fitz.open()

  for pdf in pdf_list:
    doc = fitz.open(pdf)
    merged_pdf.insert_pdf(doc)

  merged_pdf.save(output_name)
  merged_pdf.close()

  

  print("Merged the pdfs")


pdf_list = ["Airbnb Policies.pdf","hackStatement.pdf"]

merge_pdfs(pdf_list,"merged.pdf")


