import os
from strands import Agent
from strands.types.content import Message, Messages, ContentBlock
from strands.types.media import DocumentContent, DocumentSource
from strands.models.openai import OpenAIModel
from config import MODEL_ID, PROMPT_PATH
from dotenv import load_dotenv
load_dotenv()

print(f"OPENAI_API_KEY found: {'OPENAI_API_KEY' in os.environ}")


def read_system_prompt() -> str:
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_PATH}")
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def validate_pdf(pdf_path: str) -> bool:
    if not os.path.exists(pdf_path):
        raise ValueError(f"File not found: {pdf_path}")
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError(f"File must be a PDF: {pdf_path}")
    return True


def load_pdf(pdf_path: str) -> bytes:
    validate_pdf(pdf_path)
    with open(pdf_path, "rb") as f:
        return f.read()


def initialize_agent() -> Agent:
    prompt = read_system_prompt()
    model = OpenAIModel(model_id=MODEL_ID)
    return Agent(model=model, system_prompt=prompt)


def build_initial_message(pdf_bytes: bytes, file_name: str) -> Message:
        return Message(
            role="user",
            content=[
                ContentBlock(
                    document=DocumentContent(
                        format="pdf",
                        name=file_name,
                        source=DocumentSource(bytes=pdf_bytes)
                    )
                ),
                ContentBlock(
                    text="Analyze the PDF and provide a summary."
                )
            ]
        )

