import pypdf
import sys

def make_sure_each_page_is_8_5_x_11(pdf_file):
  """Makes sure each page in a PDF is 8.5 x 11.

  Args:
    pdf_file: The path to the PDF file.
  """

  pdf_reader = pypdf.PdfReader(pdf_file)
  pdf_writer = pypdf.PdfWriter()

  for page in pdf_reader.pages:
    # Set the scale of the page.  612 by 792 is 8.5 by 11 inches
    page.scale_to(612, 792)

    # Add the page to the PDF writer.
    pdf_writer.add_page(page)

  # Write the PDF to a file.
  with open(pdf_file, "wb") as f:
    pdf_writer.write(f)

if __name__ == "__main__":
  make_sure_each_page_is_8_5_x_11(sys.argv[1])