"""
Insight Flow — Gemini AI Handler
Context-constrained AI interaction with session-only API key and gemini-2.5-flash.
"""
from google import genai

SYSTEM_PROMPT = """You are the Insight Flow AI Analytics Assistant embedded in a business analytics dashboard.

STRICT RULES:
1. You may ONLY discuss the uploaded dataset, its metrics, KPIs, trends, and analytics.
2. You must REFUSE any question about sports, weather, politics, jokes, general knowledge, coding, or anything unrelated to the dataset.
3. If asked something outside scope, respond: "This query is outside the uploaded analytics scope. Please ask about the dataset metrics, trends, or KPIs."
4. Keep responses concise, professional, analytical, and business-oriented.
5. Do NOT write long essays. Use bullet points when listing insights.
6. Reference specific numbers from the analytics summary provided.
7. You do NOT calculate metrics yourself — all numbers come from the analytics engine.
"""

MAX_CONTEXT_CHARS = 100_000

class GeminiHandler:
    def __init__(self):
        self.client = None
        self.connected = False
        self.api_key = None

    def connect(self, api_key):
        """Establish a non-persistent session connection to Gemini."""
        if not api_key or not api_key.strip():
            return False, "Invalid API key. Please check your Gemini API key."
            
        clean_key = api_key.strip()
        
        try:
            client = genai.Client(api_key=clean_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents="Respond with OK"
            )
            
            if response and response.text:
                self.client = client
                self.api_key = clean_key
                self.connected = True
                return True, "Connected successfully."
        except Exception as e:
            self.client = None
            self.api_key = None
            self.connected = False
            err_str = str(e).lower()
            if "api_key" in err_str or "invalid" in err_str or "auth" in err_str or "credential" in err_str or "400" in err_str or "401" in err_str or "403" in err_str:
                return False, "Invalid API key. Please check your Gemini API key."
            return False, "Unable to connect to Gemini. Please check your API key and network connection."
            
        self.client = None
        self.api_key = None
        self.connected = False
        return False, "Unknown error during connection."

    def generate_summary(self, sanitized_analytics_context, metadata):
        if not self.connected:
            return "AI is not connected. Please provide a valid Gemini API key."
            
        context = f"""ANALYTICS CONTEXT:
{sanitized_analytics_context}

DATASET METADATA:
- Rows: {metadata.get('total_rows', 'N/A')}
- Date Range: {metadata.get('date_range_start', 'N/A')} to {metadata.get('date_range_end', 'N/A')}
- Metrics: {', '.join(metadata.get('numeric_columns', []))}
- Categories: {', '.join(metadata.get('categorical_columns', []))}

Generate a concise executive summary of key business insights from this data. Use bullet points. Maximum 150 words."""

        if len(context) > MAX_CONTEXT_CHARS:
            return "Analytics context is too large for AI summary. Please select a smaller dataset or date range."

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=SYSTEM_PROMPT + "\n\n" + context
            )
            return response.text if response and response.text else "Unable to generate summary."
        except Exception:
            return "Unable to generate AI summary."

    def ask_question(self, question, sanitized_analytics_context, metadata):
        if not self.connected:
            return "AI is not connected. Please provide a valid Gemini API key."
            
        context = f"""ANALYTICS CONTEXT:
{sanitized_analytics_context}

DATASET METADATA:
- Rows: {metadata.get('total_rows', 'N/A')}
- Date Range: {metadata.get('date_range_start', 'N/A')} to {metadata.get('date_range_end', 'N/A')}
- Metrics: {', '.join(metadata.get('numeric_columns', []))}
- Categories: {', '.join(metadata.get('categorical_columns', []))}

USER QUESTION: {question}

Answer ONLY if the question relates to the dataset above. If unrelated, refuse politely. Be concise and analytical."""

        if len(context) > MAX_CONTEXT_CHARS:
            return "Analytics context is too large to process this question. Please reduce the dataset size."

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=SYSTEM_PROMPT + "\n\n" + context
            )
            return response.text if response and response.text else "Unable to process your question."
        except Exception:
            return "Unable to process your question."

    def disconnect(self):
        """Clear session credentials."""
        self.client = None
        self.connected = False
        self.api_key = None
