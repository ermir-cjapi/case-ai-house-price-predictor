import requests
import json

def query_triton_llm(prompt: str, max_tokens: int = 100, temperature: float = 0.7, top_p: float = 0.9):
    """
    Query the Triton LLM server with a prompt.
    
    Args:
        prompt: The input text prompt
        max_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature (0.0 to 1.0)
        top_p: Nucleus sampling parameter
        
    Returns:
        The generated text response
    """
    url = "https://nvidia-triton-inference.ccrolabs.com/v2/models/llama31-8b/infer"
    
    payload = {
        "inputs": [
            {
                "name": "prompts",
                "shape": [1, 1],
                "datatype": "BYTES",
                "data": [prompt]
            },
            {
                "name": "max_output_len",
                "shape": [1, 1],
                "datatype": "INT64",
                "data": [max_tokens]
            },
            {
                "name": "temperature",
                "shape": [1, 1],
                "datatype": "FP32",
                "data": [temperature]
            },
            {
                "name": "top_p",
                "shape": [1, 1],
                "datatype": "FP32",
                "data": [top_p]
            },
            {
                "name": "output_context_logits",
                "shape": [1, 1],
                "datatype": "BOOL",
                "data": [False]
            },
            {
                "name": "output_generation_logits",
                "shape": [1, 1],
                "datatype": "BOOL",
                "data": [False]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, verify=True)
        response.raise_for_status()
        
        result = response.json()
        # Extract the generated text from the response
        if "outputs" in result:
            for output in result["outputs"]:
                if output["name"] == "outputs":
                    return output["data"][0]
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling Triton server: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "What is AI?"
    response = query_triton_llm(prompt, max_tokens=100, temperature=0.7, top_p=0.9)
    
    if response:
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
    else:
        print("Failed to get response from server")
