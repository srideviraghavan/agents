from typing import Dict, Any
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class GetWeatherInput(BaseModel):
    """Input schema for getting weather information"""
    location: str = Field(description="The location to get weather for (e.g., city name)")


def get_weather(location: str) -> Dict[str, Any]:
    """
    Get weather information for a given location.
    
    Args:
        location: The location to get weather for (e.g., city name)
        
    Returns:
        A dictionary containing mocked weather data
    """
    # Mocked weather response
    return {
        "location": location,
        "temperature": 72,
        "condition": "Partly Cloudy",
        "humidity": 65,
        "wind_speed": 10,
        "feels_like": 70,
        "description": f"Mocked weather data for {location}"
    }


class GetForecastInput(BaseModel):
    """Input schema for getting weather forecast"""
    location: str = Field(description="The location to get forecast for")
    days: int = Field(default=5, description="Number of days to forecast (default: 5)")


def get_forecast(location: str, days: int = 5) -> Dict[str, Any]:
    """
    Get weather forecast for a given location.
    
    Args:
        location: The location to get forecast for
        days: Number of days to forecast (default: 5)
        
    Returns:
        A dictionary containing mocked forecast data
    """
    # Mocked forecast response
    forecast = []
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Clear"]
    
    for i in range(days):
        forecast.append({
            "day": i + 1,
            "temperature": 70 + (i % 10),
            "condition": conditions[i % len(conditions)],
            "humidity": 60 + (i % 20)
        })
    
    return {
        "location": location,
        "forecast_days": days,
        "forecast": forecast,
        "description": f"Mocked {days}-day forecast for {location}"
    }


class WeatherTool:
    """A tool for fetching weather information with mocked responses."""
    
    @staticmethod
    def get_tools():
        """Return a list of all weather tools"""
        return [
            StructuredTool.from_function(
                func=get_weather,
                name="get_weather",
                description="Get weather information for a given location",
                args_schema=GetWeatherInput
            ),
            StructuredTool.from_function(
                func=get_forecast,
                name="get_forecast",
                description="Get weather forecast for a given location",
                args_schema=GetForecastInput
            )
        ]
