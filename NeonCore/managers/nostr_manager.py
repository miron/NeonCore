# Pseudocode
import json
from nostr import Nostr


class NostrManager:
    def __init__(self, nostr: Nostr):
        self.nostr = nostr

    def get_text_by_id(self, note_id: str) -> str:
        note = self.nostr.get_note_by_id(note_id)
        if note and "text" in note:
            return note["text"]
        else:
            return ""

    def save_text(self, text: str) -> str:
        note = {"text": text}
        note_id = self.nostr.save_note(json.dumps(note))
        return note_id

    def authenticate(self, private_key: str):
        self.nostr.authenticate(private_key)

    def get_auth_address(self) -> str:
        return self.nostr.get_auth_address()
