from transformers import pipeline

class SummarizerService:
    def __init__(self):
        # We use a smaller model for faster local execution.
        self.summarizer = None
        self.load_model()

    def load_model(self):
        try:
            print("Loading summarization model...")
            self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.summarizer = None

    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        if not self.summarizer:
            print("Summarization model not loaded. Attempting to load it now...")
            self.load_model()
            if not self.summarizer:
                raise ValueError("Summarization model is not loaded.")
        
        input_length = len(text.split())
        if input_length < min_length:
            return text
        
        actual_max_length = min(max_length, int(input_length * 0.8))
        actual_min_length = min(min_length, int(input_length * 0.2))
        
        # Model handles roughly 1024 tokens max. If the document is too long, we might need chunking.
        # For simplicity, we just truncate string to first 3000 chars roughly.
        if len(text) > 3000:
            text = text[:3000]

        try:
            result = self.summarizer(text, max_length=actual_max_length, min_length=actual_min_length, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            raise ValueError(f"Summarization failed: {e}")

ai_service = SummarizerService()
