"""
CalculatorTool - A LangChain tool for basic arithmetic operations
"""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class AddInput(BaseModel):
    """Input schema for addition"""
    a: float = Field(description="First number to add")
    b: float = Field(description="Second number to add")


def add(a: float, b: float) -> str:
    """Add two numbers"""
    result = a + b
    return f"{a} + {b} = {result}"


class SubtractInput(BaseModel):
    """Input schema for subtraction"""
    a: float = Field(description="Number to subtract from")
    b: float = Field(description="Number to subtract")


def subtract(a: float, b: float) -> str:
    """Subtract two numbers"""
    result = a - b
    return f"{a} - {b} = {result}"


class MultiplyInput(BaseModel):
    """Input schema for multiplication"""
    a: float = Field(description="First number to multiply")
    b: float = Field(description="Second number to multiply")

def multiply(a: float, b: float) -> str:
    """Multiply two numbers"""
    result = a * b
    return f"{a} * {b} = {result}"


class DivideInput(BaseModel):
    """Input schema for division"""
    a: float = Field(description="Number to divide")
    b: float = Field(description="Number to divide by")


def divide(a: float, b: float) -> str:
    """Divide two numbers"""
    if b == 0:
        return "Error: Cannot divide by zero"
    result = a / b
    return f"{a} / {b} = {result}"


class CalculatorTool:
    """A collection of calculator tools"""
    
    @staticmethod
    def get_tools():
        """Return a list of all calculator tools"""
        return [
            StructuredTool.from_function(
                func=add,
                name="add",
                description="Add two numbers",
                args_schema=AddInput
            ),
            StructuredTool.from_function(
                func=subtract,
                name="subtract",
                description="Subtract two numbers",
                args_schema=SubtractInput
            ),
            StructuredTool.from_function(
                func=multiply,
                name="multiply",
                description="Multiply two numbers",
                args_schema=MultiplyInput
            ),
            StructuredTool.from_function(
                func=divide,
                name="divide",
                description="Divide two numbers",
                args_schema=DivideInput
            )
        ]
