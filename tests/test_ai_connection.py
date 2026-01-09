import unittest
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env from project root
# (Assuming .env is in root, load_dotenv() usually finds it if run from root)
load_dotenv()

class TestAIConnection(unittest.TestCase):
    @unittest.skip("Manual test only - requires API key")
    def test_list_models(self):
        """Test connection to Gemini API allows listing models"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.skipTest("GEMINI_API_KEY not found in environment")
            
        genai.configure(api_key=api_key)
        
        try:
            models = list(genai.list_models())
            found_generate = False
            print("\nAvailable Gemini Models:")
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
                    found_generate = True
            
            self.assertTrue(found_generate, "No models with generateContent capability found")
            
        except Exception as e:
            self.fail(f"API connection failed: {e}")

if __name__ == "__main__":
    unittest.main()
