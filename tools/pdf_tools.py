from typing import Optional
import pypdf

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extracts text content from a given PDF file path using PyPDF.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        Optional[str]: The extracted text content, or None if an error occurs.
    """
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def clean_text(text: str) -> str:
    """
    Cleans and preprocesses extracted text for better summaries/quizzes.
    This is a basic cleaning function that can be expanded later.

    Args:
        text (str): The input text to clean.

    Returns:
        str: The cleaned text.
    """
    # Remove multiple spaces, newlines, and strip whitespace
    cleaned_text = " ".join(text.split())
    return cleaned_text

if __name__ == "__main__":
    # Example usage (for testing purposes)
    pdf_file = "temp_pdfs/hair_routine_schedule.pdf" # Make sure this PDF exists for testing
    extracted_text = extract_text_from_pdf(pdf_file)
    if extracted_text:
        print("--- Extracted Text ---")
        # print(extracted_text[:500]) # Print first 500 characters
        cleaned_text = clean_text(extracted_text)
        print("\n--- Cleaned Text (first 500 chars) ---")
        print(cleaned_text[:500])
    else:
        print(f"Failed to extract text from {pdf_file}")