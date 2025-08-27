from agents import input_guardrail,GuardrailFunctionOutput,RunContextWrapper

@input_guardrail
async def indian_queries(ctx:RunContextWrapper,agent,input_data:str)->GuardrailFunctionOutput:
    
    indian_cities = ["mumbai", "delhi", "bangalore", "chennai", 
        "kolkata", "hyderabad", "pune", "jaipur", "ahmedabad", "lucknow"]
   
    # Extract latest message (last user input)
    if isinstance(input_data, list) and len(input_data) > 0:
        latest_message = input_data[-1].get("content", "").lower()
    else:
        latest_message = str(input_data).lower()
    
    #print("🟢 Guardrail check on latest:", latest_message)
    
    if any(city in latest_message for city in indian_cities)or "india" in latest_message:
        
        #print("❌ Blocked Indian query")
        return GuardrailFunctionOutput(
            output_info="❌ Queries about Indian cities are not allowed.",
            tripwire_triggered=True
        )
        
    print("✅ Allowed query")
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )
    