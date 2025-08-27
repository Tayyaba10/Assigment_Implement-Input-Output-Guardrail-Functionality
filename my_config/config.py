import os
from dotenv import load_dotenv
from agents import AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig
from guardrail.input_guardrail import indian_queries
from guardrail.output_guardrail import us_output_cities

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

client = AsyncOpenAI(api_key=api_key,base_url=base_url)

MODEL = OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=client)
#run_config = RunConfig(model=MODEL)
run_config = RunConfig(
    model=MODEL,
    input_guardrails=[indian_queries],
    output_guardrails=[us_output_cities],   # future me agar chahiye to add kar sakte ho
    
)