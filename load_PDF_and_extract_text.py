from PyPDF2 import PdfReader

# Load the PDF and extract the text
pdf_path = "/mnt/data/Rich_and_Free_ebook.pdf"
reader = PdfReader(pdf_path)

# Extract text from all pages
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Show the first few hundred characters for context
full_text[:2000]

# Save the extracted text to a file
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)
