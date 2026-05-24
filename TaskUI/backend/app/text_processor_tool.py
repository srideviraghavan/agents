"""
TextProcessorTool - A LangChain tool for text processing operations
"""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class ToUppercaseInput(BaseModel):
    """Input schema for converting text to uppercase"""
    text: str = Field(description="The text to convert to uppercase")


def to_uppercase(text: str) -> str:
    """Convert the given text to uppercase"""
    return text.upper()


class ToLowercaseInput(BaseModel):
    """Input schema for converting text to lowercase"""
    text: str = Field(description="The text to convert to lowercase")


def to_lowercase(text: str) -> str:
    """Convert the given text to lowercase"""
    return text.lower()


class WordCountInput(BaseModel):
    """Input schema for counting words in text"""
    text: str = Field(description="The text to count words in")


def word_count(text: str) -> str:
    """Count the number of words in the given text"""
    words = text.split()
    count = len(words)
    return f"Word count: {count}"


class TextProcessorTool:
    """A collection of text processing tools"""
    
    @staticmethod
    def get_tools():
        """Return a list of all text processing tools"""
        return [
            StructuredTool.from_function(
                func=to_uppercase,
                name="to_uppercase",
                description="Convert the given text to uppercase",
                args_schema=ToUppercaseInput
            ),
            StructuredTool.from_function(
                func=to_lowercase,
                name="to_lowercase",
                description="Convert the given text to lowercase",
                args_schema=ToLowercaseInput
            ),
            StructuredTool.from_function(
                func=word_count,
                name="word_count",
                description="Count the number of words in the given text",
                args_schema=WordCountInput
            )
        ]
