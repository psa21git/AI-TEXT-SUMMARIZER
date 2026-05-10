import os
import requests

class SummarizerService:
    def __init__(self):
        self.hf_api_token = os.environ.get("HF_API_TOKEN")
        self.summarizer = None
        if not self.hf_api_token:
            self.load_local_model()

    def load_local_model(self):
        try:
            print("No HF_API_TOKEN found. Loading local summarization model...")
            # We import transformers only locally to save RAM on Render!
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

        if self.hf_api_token:
            print("Using Hugging Face Inference API...")
            headers = {"Authorization": f"Bearer {self.hf_api_token}"}
            API_URL = "https://api-inference.huggingface.co/models/Falconsai/text_summarization"
            payload = {
                "inputs": text,
                "parameters": {"max_length": actual_max_length, "min_length": actual_min_length, "do_sample": False}
            }
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()[0]['summary_text']
            else:
                raise ValueError(f"HF API Error: {response.text}")
        else:
            if not self.summarizer:
                print("Local model not loaded. Attempting to load it now...")
                self.load_local_model()
                if not self.summarizer:
                    raise ValueError("Summarization model is not loaded (OOM Memory Error). Please provide an HF_API_TOKEN.")
            try:
                result = self.summarizer(text, max_length=actual_max_length, min_length=actual_min_length, do_sample=False)
                return result[0]['summary_text']
            except Exception as e:
                raise ValueError(f"Summarization failed: {e}")

ai_service = SummarizerService()
