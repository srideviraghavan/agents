"""
Simple React Agent that uses TextProcessor and Calculator tools
"""

import os
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from app.text_processor_tool import TextProcessorTool
from app.calculator_tool import CalculatorTool
from app.weather_tool import WeatherTool

class TaskProcessorRouterAgent:
    """A simple React agent with TextProcessor and Calculator tools"""
    
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0, base_url: str ="https://your-custom-endpoint.com"):
        """
        Initialize the React agent
        
        Args:
            model_name: Name of the OpenAI model to use
            temperature: Temperature for the model
        """
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        # Initialize the LLM
        self.llm = ChatOpenAI(model=model_name, temperature=temperature, base_url=base_url, api_key="not-needed")
        
        self.prompt = hub.pull("hwchase17/openai-tools-agent")

        text_tools = TextProcessorTool.get_tools()
        calc_tools = CalculatorTool.get_tools()
        weather_tools = WeatherTool.get_tools()
        self.tools = text_tools + calc_tools + weather_tools        

        router_agent = create_tool_calling_agent(
            llm=self.llm,          # same or different LLM
            tools=self.tools,
            prompt=self.prompt
        )

        self.router_executor = AgentExecutor(
            agent=router_agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=100,
            max_execution_time=180
        )   

    
    def run(self, query: str) -> str:
        """
        Run the agent with a query
        
        Args:
            query: The user's query/question
            
        Returns:
            The agent's response
        """
        result = self.router_executor.invoke({"input": query})
        return result["output"]
    
    def get_tool_names(self) -> list:
        """Get list of available tool names"""
        return [tool.name for tool in self.tools]