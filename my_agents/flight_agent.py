# class10
from agents import Agent,function_tool
from guardrail.input_guardrail import indian_queries
from guardrail.output_guardrail import us_output_cities

@function_tool
def find_flight(from_city:str,to_city:str,data:str)->str:
    return f"flight PK100 available from {from_city} to {to_city} on {data} price are PK28000."
    
flight_agent =Agent(
    name="flight Agent",
    instructions="You are a flight agent, find best and cheap flights between two cities.",
    tools=[find_flight],
    handoff_description="find best flight between two cities.",
    input_guardrails=[indian_queries],
    output_guardrails=[us_output_cities],
)