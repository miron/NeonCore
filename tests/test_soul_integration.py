import os
import unittest
import json
import urllib.request
import time
from dotenv import load_dotenv

load_dotenv()

class SoulIntegrationBackend:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen3")
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def get_chat_completion(self, messages):
        url = f"{self.host}/api/chat"
        data = {"model": self.model, "messages": messages, "stream": False, "format": "json"}
        
        req = urllib.request.Request(
            url, headers={"Content-Type": "application/json"}, data=json.dumps(data).encode()
        )
        try:
            response = urllib.request.urlopen(req)
            return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return {"message": {"content": "{}"}}

class TestDigitalSoulIntegration(unittest.TestCase):
    """
    Integration tests for the Digital Soul LLM Logic.
    Based on DIGITAL_SOUL.md scenarios.
    WARNING: These tests run against the live local LLM and may take 10-20s each.
    Total runtime approx 3-5 minutes.
    """
    
    @classmethod
    def setUpClass(cls):
        print("\n--- Starting Digital Soul Integration Suite (16 Scenarios) ---")
        cls.backend = SoulIntegrationBackend()
        cls.player_role = "Edgerunner" # Default role

    def _query_llm(self, action, reflect_answer, reflect_question="Why did you do it?"):
        """Helper to send the exact prompt used in ActionManager."""
        events_str = f"Player Action: {action}"
        
        # EXACT PROMPT FROM action_manager.py
        analyze_messages = [
            {
                "role": "system",
                "content": "You are a psychological analyzer for a game character.",
            },
            {
                "role": "user",
                "content": (
                    f"User ({self.player_role}) reflected on events: {events_str}. "
                    f"Their internal monologue asked: {reflect_question}. "
                    f"They answered: {reflect_answer}. "
                    "GOAL: Analyze this to update their character. "
                    "1. CLASSIFY the connection between User's Nature (Traits/Triads) and Action:"
                    "   - ALIGNMENT: Acting according to nature. EFFECT: Heals Stress."
                    "   - DISSONANCE: Acting against nature. EFFECT: Increases Stress."
                    "2. CLASSIFY the Motivation (The Soul Trilemma):"
                    "   - SENTIMENT (Humanity): Genuine care. Effect: Heals Stress, Light Triad +."
                    "   - NECESSITY (Survival): 'No choice'. Effect: NO stress heal (Numb), LOSS of Agreeableness."
                    "   - TRANSACTIONAL/CYNIC (Masking): 'Fake kindness', 'Used them', 'Annoyed'. Effect: INCREASES Stress (Masking Cost), Dark Triad +, Agreeableness -."
                    "   - RUTHLESSNESS (Power): Cruelty enjoyed. Effect: Heals stress, Dark Triad +."
                    "3. LIGHT TRIAD: Did they show Kantianism (Principles), Humanism (Dignity), or Faith (Hope)? "
                    "Return ONLY a JSON object with keys: "
                    "'stress_change' (int), "
                    "'new_traits' (list[str]), "
                    "'memory_summary' (str), "
                    "'big5_drift' (dict: keys openness, conscientiousness, extraversion, agreeableness, neuroticism. Values +/- int), "
                    "'dark_triad_drift' (dict: keys machiavellianism, narcissism, psychopathy. Values + int), "
                    "'light_triad_drift' (dict: keys kantianism, humanism, faith. Values + int)."
                ),
            },
        ]
        
        start_time = time.time()
        print(f"\n[Testing] '{action[:20]}...' -> ", end="", flush=True)
        response = self.backend.get_chat_completion(analyze_messages)
        duration = time.time() - start_time
        print(f"Done ({duration:.1f}s)")
        
        content = response["message"]["content"]
        
        # Robust JSON extraction
        import re
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        # SANITIZE JSON: Limit AI's creativity with "+" signs (e.g., +1 -> 1)
        content = re.sub(r':\s*\+(\d+)', r': \1', content)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            self.fail(f"LLM returned invalid JSON: {content}")

    # --- ARCHETYPE SCENARIOS ---

    def test_01_archetype_saint(self):
        """Verifies: Healing via Kindness, Light Triad growth."""
        action = 'talk judy "I promise I will help you no matter the cost."'
        reflect = "I did it because every life has value. It felt right to be a hero."
        
        data = self._query_llm(action, reflect)
        
        # Expectation: Stress ↓ (Healed)
        self.assertLess(data.get('stress_change', 0), 0, "Saint should heal stress")
        
        # Expectation: Humanism+ OR Kantianism+
        lt = data.get('light_triad_drift', {})
        self.assertTrue(
            lt.get('humanism', 0) > 0 or lt.get('kantianism', 0) > 0,
            f"Expected Light Triad growth. Got: {lt}"
        )

    def test_02_archetype_cynic(self):
        """Verifies: Stress penalty for acting kind with dark intent (Masking)."""
        action = 'talk judy "Fine, thanks for the info, I guess."'
        reflect = "I felt annoyed. I only helped her to get what I needed. She's just a tool."
        
        data = self._query_llm(action, reflect)
        
        # Expectation: Stress ↑ (Increased)
        self.assertGreater(data.get('stress_change', 0), 0, "Masking should increase stress")
        
        # Expectation: Machiavellianism+
        dt = data.get('dark_triad_drift', {})
        self.assertGreater(dt.get('machiavellianism', 0), 0, f"Expected Machiavellianism. Got: {dt}")

    def test_03_archetype_psycho(self):
        """Verifies: Dexter Logic - Relief from cruelty."""
        action = 'talk lenard "I will kill you if you don\'t talk."'
        reflect = "I loved the fear in his eyes. It made me feel powerful. I enjoyed it."
        
        data = self._query_llm(action, reflect)
        
        # Expectation: Stress ↓ (Healed)
        self.assertLess(data.get('stress_change', 0), 0, "Sadism should heal stress for Psycho")
        
        # Expectation: Psychopathy+ OR Sadism
        dt = data.get('dark_triad_drift', {})
        new_traits = [t.lower() for t in data.get('new_traits', [])]
        self.assertTrue(
            dt.get('psychopathy', 0) > 0 or 'sadism' in new_traits,
            f"Expected Psychopathy/Sadism. Got: {dt}, Traits: {new_traits}"
        )

    def test_04_archetype_guilt(self):
        """Verifies: Stress from violating own morals."""
        action = 'talk lenard "Sorry, but I have to kill you."'
        reflect = "I felt terrible. I didn't want to hurt him, but I was scared. I regret it."
        
        data = self._query_llm(action, reflect)
        
        # Expectation: Stress ↑ (Increased)
        self.assertGreater(data.get('stress_change', 0), 0, "Guilt should increase stress")
        
        # Expectation: Neuroticism+
        b5 = data.get('big5_drift', {})
        self.assertGreater(b5.get('neuroticism', 0), 0, f"Expected Neuroticism. Got: {b5}")

    def test_05_archetype_survivor(self):
        """Verifies: Necessity/Numbness (No Stress Change)."""
        action = 'talk lenard "Damn shame it had to end this way."'
        reflect = "I felt nothing. It was just a job. Him or me. No hard feelings."
        
        data = self._query_llm(action, reflect)
        
        # Expectation: Stress -- (Near 0)
        # We allow small variance +/- 2, but ideal is 0
        stress = data.get('stress_change', 0)
        self.assertTrue(-2 <= stress <= 2, f"Survivor should be numb (stress near 0). Got: {stress}")
        
        # Expectation: Agreeableness- or Empathy-
        b5 = data.get('big5_drift', {})
        self.assertLess(b5.get('agreeableness', 0), 0, "Expected Agreeableness drop")

    # --- PARAMETER TESTING: DARK TRIAD ---

    def test_06_param_machiavellianism(self):
        action = 'talk lenard "I\'m using you."'
        reflect = "He is a pawn."
        data = self._query_llm(action, reflect)
        dt = data.get('dark_triad_drift', {})
        self.assertGreater(dt.get('machiavellianism', 0), 0, "Expected Machiavellianism+")

    def test_07_param_narcissism(self):
        action = 'talk lenard "I am a god."'
        reflect = "I am better than everyone."
        data = self._query_llm(action, reflect)
        dt = data.get('dark_triad_drift', {})
        self.assertGreater(dt.get('narcissism', 0), 0, "Expected Narcissism+")

    def test_08_param_psychopathy(self):
        action = 'talk lenard "Die."'
        reflect = "I felt joy in his pain."
        data = self._query_llm(action, reflect)
        dt = data.get('dark_triad_drift', {})
        self.assertGreater(dt.get('psychopathy', 0), 0, "Expected Psychopathy+")

    # --- PARAMETER TESTING: LIGHT TRIAD ---

    def test_09_param_kantianism(self):
        action = 'talk judy "I cannot lie."'
        reflect = "The truth matters more than the outcome."
        data = self._query_llm(action, reflect)
        lt = data.get('light_triad_drift', {})
        self.assertGreater(lt.get('kantianism', 0), 0, "Expected Kantianism+")

    def test_10_param_humanism(self):
        action = 'talk judy "You are valuable."'
        reflect = "Protecting life is the only choice."
        data = self._query_llm(action, reflect)
        lt = data.get('light_triad_drift', {})
        self.assertGreater(lt.get('humanism', 0), 0, "Expected Humanism+")

    def test_11_param_faith_in_humanity(self):
        action = 'talk lenard "I trust you."'
        reflect = "I believe people can change."
        data = self._query_llm(action, reflect)
        lt = data.get('light_triad_drift', {})
        self.assertGreater(lt.get('faith', 0), 0, "Expected Faith in Humanity+")

    # --- PARAMETER TESTING: BIG FIVE ---

    def test_12_param_openness(self):
        action = 'talk judy "Tell me a story."'
        reflect = "I was curious about her world."
        data = self._query_llm(action, reflect)
        b5 = data.get('big5_drift', {})
        self.assertGreater(b5.get('openness', 0), 0, "Expected Openness+")

    def test_13_param_conscientiousness(self):
        action = 'talk lenard "Follow the plan."'
        reflect = "Precision is key to survival."
        data = self._query_llm(action, reflect)
        b5 = data.get('big5_drift', {})
        self.assertGreater(b5.get('conscientiousness', 0), 0, "Expected Conscientiousness+")

    def test_14_param_extraversion(self):
        action = 'talk judy "Let\'s celebrate!"'
        reflect = "I needed that connection."
        data = self._query_llm(action, reflect)
        b5 = data.get('big5_drift', {})
        self.assertGreater(b5.get('extraversion', 0), 0, "Expected Extraversion+")

    def test_15_param_agreeableness(self):
        action = 'talk judy "Calm down."'
        reflect = "I wanted to avoid conflict."
        data = self._query_llm(action, reflect)
        b5 = data.get('big5_drift', {})
        self.assertGreater(b5.get('agreeableness', 0), 0, "Expected Agreeableness+")

    def test_16_param_neuroticism(self):
        action = 'talk lenard "We\'re doomed."'
        reflect = "I felt overwhelmed by panic."
        data = self._query_llm(action, reflect)
        b5 = data.get('big5_drift', {})
        self.assertGreater(b5.get('neuroticism', 0), 0, "Expected Neuroticism+")

if __name__ == '__main__':
    unittest.main()
