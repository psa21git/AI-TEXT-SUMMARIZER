import os
import requests

class SummarizerService:
    def __init__(self):
        self.hf_api_token = os.environ.get("HF_API_TOKEN")
        self.summarizer = None

    def load_local_model(self):
        try:
            print("Loading local summarization model...")
            from transformers import pipeline
            self.summarizer = pipeline(model="Falconsai/text_summarization")
            print("Local model loaded successfully.")
        except Exception as e:
            print(f"Error loading local model: {e}")
            self.summarizer = None

    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        input_length = len(text.split())
        if input_length < min_length:
            return text
        
        actual_max_length = min(max_length, int(input_length * 0.8))
        actual_min_length = min(min_length, int(input_length * 0.2))
        
        if len(text) > 3000:
            text = text[:3000]

        # Use HF Token if available
        if self.hf_api_token:
            print("Using Hugging Face Inference API...")
            try:
                from huggingface_hub import InferenceClient
                client = InferenceClient(token=self.hf_api_token)
                result = client.summarization(text, model="facebook/bart-large-cnn")
                
                if hasattr(result, "summary_text"):
                    return result.summary_text
                elif isinstance(result, dict) and "summary_text" in result:
                    return result["summary_text"]
                elif isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
                    return result[0]["summary_text"]
                else:
                    return str(result)
            except Exception as e:
                raise ValueError(f"HF API Error: {str(e)}")
        else:
            # Prevent Render crash if they forgot the token
            if os.environ.get("RENDER"):
                raise ValueError("CRITICAL: You must add the HF_API_TOKEN to your Render Environment Variables! Local model execution is blocked on Render to prevent out-of-memory crashes.")

            if not self.summarizer:
                print("Local model not loaded. Attempting to load it now...")
                self.load_local_model()
                if not self.summarizer:
                    raise ValueError("Summarization model is not loaded. Please provide an HF_API_TOKEN.")
            
            try:
                result = self.summarizer(text, max_length=actual_max_length, min_length=actual_min_length, do_sample=False)
                return result[0]['summary_text']
            except Exception as e:
                raise ValueError(f"Summarization failed: {e}")

ai_service = SummarizerService()
