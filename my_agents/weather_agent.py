# class10
from agents import Agent,function_tool
from guardrail.input_guardrail import indian_queries
from guardrail.output_guardrail import us_output_cities

@function_tool
def find_weather(city:str)->str:
    return f"{city} tempertaure is 35 degree."
    
weather_agent = Agent(
    name="weather Agent",
    instructions="You are a weather agent,use tool find_weather to get the weather of provided city",
    tools=[find_weather],
    handoff_description="get the weather of provided city", 
    input_guardrails=[indian_queries],
    output_guardrails=[us_output_cities]
)