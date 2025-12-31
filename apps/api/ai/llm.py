"""
LLM service using Llama 3 via Ollama or OpenAI
For jargon simplification and smart drafting
"""
import requests
from openai import OpenAI
from django.conf import settings


class LLMClient:
    """
    Client for LLM operations (Llama 3 via Ollama or OpenAI as fallback)
    """
    
    def __init__(self, use_ollama=True):
        self.use_ollama = use_ollama
        self.ollama_url = "http://localhost:11434"  # Default Ollama URL
        self.openai_client = None
        
        if not use_ollama and settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def _call_ollama(self, prompt, model="llama3"):
        """Call Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json().get('response', '')
        except Exception as e:
            print(f"Ollama error: {e}")
            raise
    
    def _call_openai(self, prompt, model="gpt-3.5-turbo"):
        """Call OpenAI API as fallback"""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
            raise
    
    def generate(self, prompt):
        """Generate text from prompt"""
        if self.use_ollama:
            try:
                return self._call_ollama(prompt)
            except:
                # Fallback to OpenAI if Ollama fails
                if self.openai_client:
                    return self._call_openai(prompt)
                raise
        else:
            return self._call_openai(prompt)
    
    def simplify_jargon(self, text, language='en'):
        """
        Convert government jargon to plain language
        
        Args:
            text: Complex government text
            language: Target language code
        
        Returns:
            Simplified text
        """
        prompt = f"""You are a helpful assistant that simplifies government and legal jargon for common citizens.

Convert the following text into simple, easy-to-understand language that a person with basic education can comprehend. Keep it concise (3-5 bullet points).

Text: {text}

Simplified version:"""
        
        return self.generate(prompt)
    
    def draft_complaint_letter(self, issue_details):
        """
        Generate a formal complaint letter
        
        Args:
            issue_details: Dict with keys: issue, location, officer_name, officer_designation
        
        Returns:
            Formatted complaint letter
        """
        prompt = f"""You are a legal assistant helping citizens write formal complaint letters to government officials.

Write a professional complaint letter with the following details:
- Issue: {issue_details.get('issue', 'Civic problem')}
- Location: {issue_details.get('location', 'Not specified')}
- To: {issue_details.get('officer_name', '[Officer Name]')}, {issue_details.get('officer_designation', '[Designation]')}

The letter should:
1. Be formal and respectful
2. Clearly state the problem
3. Reference relevant Citizens Charter clauses (if applicable)
4. Request specific action
5. Mention timeline expectations

Letter:"""
        
        return self.generate(prompt)
    
    def summarize_document(self, document_text, max_points=5):
        """
        Summarize long government documents
        
        Args:
            document_text: Full document text
            max_points: Maximum bullet points
        
        Returns:
            Summarized text
        """
        prompt = f"""Summarize the following government document into {max_points} key points that a citizen needs to know:

{document_text[:2000]}  # Limit input length

Summary:"""
        
        return self.generate(prompt)
    
    def extract_action_steps(self, solution_text):
        """
        Extract actionable steps from a solution description
        
        Args:
            solution_text: Solution description
        
        Returns:
            List of action steps
        """
        prompt = f"""Extract clear, actionable steps from the following solution. Format as a numbered list.

Solution: {solution_text}

Steps:"""
        
        response = self.generate(prompt)
        
        # Parse numbered list
        steps = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                step = line.lstrip('0123456789.-) ')
                if step:
                    steps.append(step)
        
        return steps
    
    def generate_rti_query(self, topic, department):
        """
        Generate an RTI query template
        
        Args:
            topic: What information is being sought
            department: Target department
        
        Returns:
            RTI query text
        """
        prompt = f"""Generate a formal RTI (Right to Information) query for the following:

Topic: {topic}
Department: {department}

The query should:
1. Be specific and clear
2. Reference RTI Act 2005
3. Request information in a structured format
4. Include timeline (30 days as per Act)

RTI Query:"""
        
        return self.generate(prompt)


# Singleton instance
_llm_client = None

def get_llm_client(use_ollama=True):
    """Get or create LLM client instance"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient(use_ollama=use_ollama)
    return _llm_client
