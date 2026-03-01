# app/services/subscriber_service.py
"""Newsletter subscriber storage using JSON file."""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class Subscriber:
    """Subscriber data class."""

    def __init__(self, email: str, name: Optional[str] = None, source: str = "footer"):
        self.email = email.lower().strip()
        self.name = name.strip() if name else None
        self.source = source
        self.subscribed_at = datetime.now().isoformat()
        self.is_active = True

    def to_dict(self) -> Dict:
        return {
            "email": self.email,
            "name": self.name,
            "source": self.source,
            "subscribed_at": self.subscribed_at,
            "is_active": self.is_active,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Subscriber":
        sub = Subscriber(data["email"], data.get("name"), data.get("source", "footer"))
        sub.subscribed_at = data.get("subscribed_at", sub.subscribed_at)
        sub.is_active = data.get("is_active", True)
        return sub


class SubscriberService:
    """Manage newsletter subscribers using JSON file storage."""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.subscribers_file = self.data_dir / "subscribers.json"
        self._load()

    def _load(self) -> None:
        """Load subscribers from file."""
        if self.subscribers_file.exists():
            try:
                with open(self.subscribers_file, "r") as f:
                    data = json.load(f)
                    self.subscribers = {sub["email"]: Subscriber.from_dict(sub) for sub in data}
            except (json.JSONDecodeError, KeyError):
                self.subscribers = {}
        else:
            self.subscribers = {}

    def _save(self) -> None:
        """Save subscribers to file."""
        with open(self.subscribers_file, "w") as f:
            data = [sub.to_dict() for sub in self.subscribers.values()]
            json.dump(data, f, indent=2)

    def subscribe(self, email: str, name: Optional[str] = None, source: str = "footer") -> Dict:
        """Add or update a subscriber. Returns status dict."""
        email = email.lower().strip()

        # Validate email
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            return {"success": False, "message": "Please enter a valid email address."}

        # Check if already subscribed
        if email in self.subscribers:
            sub = self.subscribers[email]
            if not sub.is_active:
                sub.is_active = True
                self._save()
                return {"success": True, "message": "Welcome back! You've been re-subscribed."}
            return {"success": True, "message": "You're already on the list! We'll keep you posted."}

        # Create new subscriber
        subscriber = Subscriber(email, name, source)
        self.subscribers[email] = subscriber
        self._save()
        return {"success": True, "message": "You're in! Thanks for subscribing."}

    def get_active_subscribers(self) -> List[Subscriber]:
        """Get all active subscribers."""
        return [sub for sub in self.subscribers.values() if sub.is_active]

    def get_all_subscribers(self) -> List[Subscriber]:
        """Get all subscribers (active and inactive)."""
        return list(self.subscribers.values())

    def unsubscribe(self, email: str) -> bool:
        """Mark subscriber as inactive."""
        email = email.lower().strip()
        if email in self.subscribers:
            self.subscribers[email].is_active = False
            self._save()
            return True
        return False

    def export_csv(self) -> str:
        """Export active subscribers as CSV."""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["email", "name", "source", "subscribed_at"])
        for sub in self.get_active_subscribers():
            writer.writerow([sub.email, sub.name or "", sub.source, sub.subscribed_at])
        return output.getvalue()

    def count_active(self) -> int:
        """Get count of active subscribers."""
        return len(self.get_active_subscribers())
