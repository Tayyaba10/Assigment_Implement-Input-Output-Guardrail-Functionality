# class10
from agents import Agent,function_tool
from guardrail.input_guardrail import indian_queries
from guardrail.output_guardrail import us_output_cities

@function_tool
def find_hotel(city:str,date:str)->str:
    return f"""hotel available on {date} in {city} are following 
-PC hotel, 1 night stay rent is 15000 , breakfast included, free parking,
-Marriot hotel, 1 night stay rent is 1000, breakfast included, free parking,
-Navihotel, 1 night stay rent is 2000, wifi free.
"""
    
hotel_agent = Agent(
    name="hotel Agent",
    instructions="You are a flight agent, find best and cheap flights between two cities.",
    tools=[find_hotel],
    handoff_description="find of hotel in city.",
    input_guardrails=[indian_queries],
    output_guardrails=[]

)