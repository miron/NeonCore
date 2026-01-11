import unittest
import os
import urllib.request
from dotenv import load_dotenv

# Ensure env vars are loaded
load_dotenv()

class TestRemoteConnection(unittest.TestCase):
    """
    Optional test to verify connection to a remote Ollama instance.
    Skips if OLLAMA_HOST is not set or if the host is unreachable.
    """

    def setUp(self):
        self.host = os.environ.get("OLLAMA_HOST")
        self.model = os.environ.get("OLLAMA_MODEL")

    def test_remote_ollama_connection(self):
        if not self.host:
            self.skipTest("OLLAMA_HOST environment variable not set.")
        
        url = f"{self.host}/api/tags"
        print(f"\n[RemoteTest] Checking connection to {self.host}...")

        try:
            # Short timeout to avoid hanging tests if offline
            resp = urllib.request.urlopen(url, timeout=3)
            self.assertEqual(resp.getcode(), 200, "Failed to get 200 OK from Ollama API")
            print("✅ Remote Ollama is reachable.")
        except urllib.error.URLError as e:
            self.skipTest(f"Remote host unreachable (Optional Test): {e}")
        except Exception as e:
            self.fail(f"Unexpected error connecting to remote: {e}")

if __name__ == '__main__':
    unittest.main()
