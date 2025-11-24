from agents.tool import FunctionTool
import os
from dotenv import load_dotenv
from agents import Agent, Runner, Tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from tools.pdf_tools import extract_text_from_pdf, clean_text

load_dotenv()

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


def generate_quiz(pdf_path: str) -> str:
    # 1. Load the quiz_prompt.txt
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'quiz_prompt.txt')
    with open(prompt_path, "r") as f:
        quiz_prompt_template = f.read()

    # 2. Use pdf_tools.extract_text_from_pdf to get text.
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Optional: Clean the text
    cleaned_text = clean_text(pdf_text) # Added clean_text for consistency
    
    # 3. Initialize an OpenAgents SDK Agent
    quiz_agent = Agent(
        name="Quiz Generator",
        instructions="You are an expert educational quiz maker. who Generates multiple-choice and mixed-style quizzes with answers from PDF documents.",
        model=OpenAIChatCompletionsModel(
        model="gemini-2.5-flash", # Using a compatible Gemini model name
        openai_client=gemini_client,
    ),
    )

    # Prepare the input for the agent
    agent_input = quiz_prompt_template.format(pdf_text=cleaned_text) # Used cleaned_text

    # 4. Runs the agent to generate the quiz.
    result = Runner.run_sync(quiz_agent, agent_input)

    return result.final_output
