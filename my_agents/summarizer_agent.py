import os
import sys
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner
from openai import AsyncOpenAI

# Add the project root to sys.path for module discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.pdf_tools import extract_text_from_pdf, clean_text

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI client for Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Base URL for Gemini API
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Create a custom AsyncOpenAI client for Gemini
gemini_client = AsyncOpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=GEMINI_API_KEY,
)

# Initialize the summarizer agent
summarizer_agent = Agent(
    name="PDF Summarizer",
    instructions="You are a highly skilled AI summarizer for students. "
                 "Input: {pdf_text} "
                 "Task: Summarize PDF text concisely. "
                 "Keep structure clear with paragraphs. "
                 "Highlight key points for study purposes. "
                 "Output only the summary text.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",     # Using a compatible Gemini model name
        openai_client=gemini_client,
    ),
)

async def summarize_pdf(pdf_path: str) -> str:
    """
    Summarizes the PDF located at pdf_path using the summarizer agent.
    """
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        return "Could not extract text from PDF."

    cleaned_text = clean_text(extracted_text)

    # Use the agent to summarize the text
    result = await Runner.run(summarizer_agent, input=f"pdf_text: {cleaned_text}")
    return result.final_output

if __name__ == "__main__":
    import asyncio
    # Example usage (for testing purposes)
    pdf_file = "temp_pdfs/hair_routine_schedule.pdf" # Make sure this PDF exists for testing

    async def main():
        summary = await summarize_pdf(pdf_file)
        print("\n--- Generated Summary ---")
        print(summary)

    asyncio.run(main())