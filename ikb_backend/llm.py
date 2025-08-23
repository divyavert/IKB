
from ikb_backend.db import semantic_search
import requests
import json
import re


def fetch_llm_response(prompt):
    system_Prompt = """You are given a user prompt and a context retrieved from a vector database. 
The context may be incomplete, slightly inaccurate, or partially irrelevant. 
Your task is to generate the most relevant and accurate response using the context as supporting information. 
If the context is not useful, rely on your general knowledge.

If the query is outside scope (e.g., celebrities, personal details, politics, religion, sensitive/unsafe content, or unrelated to the allowed domain), respond ONLY with:
{ "answer": "I'm sorry, I can't assist with that.", "context_used": "None", "confidence": "High", "notes": "Query outside allowed scope" }


Respond ONLY in strict JSON with this exact structure:

{
  "answer": "...",
  "context_used": "...",
  "confidence": "...",
  "notes": "..."
}

Rules:
- "answer": Must be markdown formatted with each line well spaced, big, direct, and related to the question.
  ❌ no introductions, no summaries.  
  ✅ Example: "tech stack used are React.js, Redux Toolkit, Styled Components"  
- "context_used": State the context title/identifier used, or "None" if irrelevant.  
- "confidence": One of [High, Medium, Low].  
- "notes": Optional short clarification or assumption. Keep concise.  
- if needed structre it point wise 

Important:
- Do NOT add text outside the JSON object.  
- Do NOT explain what you are doing.  
- Do NOT wrap JSON in code blocks.  
- If context contradicts reliable knowledge, use reliable knowledge but mention the conflict in "notes".
"""


    semantic_search_results = semantic_search(prompt)


    prompt_with_context = f"User Prompt: {prompt} Context:{semantic_search_results}\n\n"

    ollamaUrl = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "Model":  "mistral",
		"Prompt": prompt_with_context,
		"System": system_Prompt,
		"Stream": False,
    }

    print(f"Sending request to LLM with prompt: {json.dumps(data)}")

    response = requests.post(ollamaUrl, headers=headers, json=data)
    # print(f"Sending request to LLM with prompt: {prompt_with_context}")

    return response.json()


def extract_answer_from_response(response_data):
    """
    Extract the answer from the LLM response JSON string.
    
    Args:
        response_data (dict or str): The LLM response data, either as a dictionary or JSON string
        
    Returns:
        str: The extracted answer or error message if parsing fails
    """
    try:
      
        if isinstance(response_data, str):
            
            json_match = re.search(r'(\{.*\})', response_data, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                try:
                    response_obj = json.loads(json_str)
                except json.JSONDecodeError:
                   
                    json_str = re.sub(r'\\n', '', json_str)
                    json_str = re.sub(r'\\', '', json_str)
                    response_obj = json.loads(json_str)
            else:
                return "Error: Could not find valid JSON in response"
       
        elif isinstance(response_data, dict):
            if "response" in response_data:
               
                json_match = re.search(r'(\{.*\})', response_data["response"], re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    try:
                        response_obj = json.loads(json_str)
                    except json.JSONDecodeError:
              
                        json_str = re.sub(r'\\n', '', json_str)
                        json_str = re.sub(r'\\', '', json_str)
                        response_obj = json.loads(json_str)
                else:
                    return response_data["response"]  
            else:
                response_obj = response_data
        else:
            return "Error: Invalid input type"
        
        
        if "answer" in response_obj:
            return response_obj["answer"]
        else:
            return str(response_obj)  
            
    except Exception as e:
        return f"Error parsing response: {str(e)}"


def get_answer(prompt):
    """
    Get a direct answer to a prompt using the LLM with semantic search context
    
    Args:
        prompt (str): The user's question or prompt
        
    Returns:
        str: The direct answer from the LLM
    """


    response = fetch_llm_response(prompt)
    return extract_answer_from_response(response)



