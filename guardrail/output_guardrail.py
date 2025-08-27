from agents import output_guardrail,GuardrailFunctionOutput,RunContextWrapper

@output_guardrail
async def us_output_cities(ctx:RunContextWrapper,agent,output_data:str)->GuardrailFunctionOutput:
    
    us_cities = [
    "new york", "los angeles", "chicago", "houston", "san francisco",
    "boston", "miami", "dallas", "seattle", "washington"
]
    text = str(output_data).lower()
    
    if any(city in text for city in us_cities):
           # print("❌ U.S. city results are blocked.")
            return GuardrailFunctionOutput(
                output_info="❌ U.S. city results are blocked.", 
                tripwire_triggered=True)

    print("✅ Allowed query")
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )
    