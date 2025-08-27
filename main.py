from agents import Agent,Runner,set_tracing_disabled,handoff,RunContextWrapper,HandoffInputData,TResponseInputItem,InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered 
import asyncio
from my_config.config import run_config
from my_agents.flight_agent import flight_agent
from my_agents.hotel_agent import hotel_agent
from my_agents.weather_agent import weather_agent
from pydantic import BaseModel
from typing import Literal
from agents.extensions import handoff_filters

set_tracing_disabled(True)

class User(BaseModel):
    name:str
    age:int
    role:Literal["admin","super user","basic"]

async def handoff_permission(ctx:RunContextWrapper[User],agent)->bool:
    if ctx.context.age > 19 and ctx.context.role == "super user":
        return True
    
    if ctx.context.role == "super user":
        return True
    
    return False

async def handoff_filter(data:HandoffInputData)->HandoffInputData:
    data = handoff_filters.remove_all_tools(data) # remove tool calling all hojaegi token save input hoga bs 
    history = data.input_history[-2:]
    
    return HandoffInputData(
        input_history=history,
        pre_handoff_items=data.pre_handoff_items,
        new_items=data.new_items
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are triage agent,hands off to flight,hotel and weather agent if user ask for
    otherwise you can response yourself.
    """,
    handoffs=[
         handoff(
             weather_agent,
             tool_name_override="handoff_weatheragent",
             tool_description_override="handoff to weather to get the weather information",
             is_enabled=handoff_permission,
             input_filter=handoff_filter,
             ),
        flight_agent,
        hotel_agent,
        weather_agent
        ],
    handoff_description="""    
    this triage agent, hand off to flight,
    hotel and weather agent if user ask for otherwise you can response yourself.
    """, 
    
)

weather_agent.handoffs.append(triage_agent)

flight_agent.handoffs.append(triage_agent)

hotel_agent.handoffs.append(triage_agent)

async def main():
    
    user = User(name="abc",role="admin",age=20)
    start_agent = triage_agent
    input_data :list[TResponseInputItem] = []
    
    while True:  
        
        user_prompt = input("enter your query: ")
        if user_prompt == "exit":
            print("GoodBye!")
            break
        
        input_data.append({
            "role":"user",
            "content":user_prompt
        })
        
        try:
            result = await Runner.run(
                start_agent,
                input=input_data,
                run_config=run_config,
                context=user,
                )
            
            start_agent = result.last_agent
        
            print(result.final_output)
            
        except InputGuardrailTripwireTriggered as e:
            print(f"Input Blocked: {e}")
            
        except OutputGuardrailTripwireTriggered as e:
            print(f"Output Blocked: {e}")
    
asyncio.run(main())