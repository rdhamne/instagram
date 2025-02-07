import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Your Instagram API access token
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")  # Your Instagram Business ID

def get_comments(reel_id):
    """Fetch comments from the given Instagram Reel."""
    url = f"https://graph.facebook.com/v19.0/{reel_id}/comments?access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        comments = response.json().get("data", [])
        return [(c["from"]["id"], c["from"].get("username", "")) for c in comments if "from" in c]
    else:
        print("Error fetching comments:", response.json())
        return []

def send_dm(user_id, message):
    """Send a direct message to a user."""
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/messages"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message},
        "access_token": ACCESS_TOKEN,
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print(f"Message sent to {user_id}")
        return True
    elif response.status_code == 400 and "rate limit" in response.text.lower():
        print("Rate limit reached. Waiting...")
        time.sleep(60)  # Wait 60 seconds before retrying
        return send_dm(user_id, message)
    else:
        print("Error sending message:", response.json())
        return False

def main():
    """Main function to fetch commenters and send messages."""
    reel_id = input("Enter Reel ID: ")
    message = input("Enter message to send: ")
    
    sent_users = set()
    while True:
        commenters = get_comments(reel_id)
        for user_id, username in commenters:
            if user_id not in sent_users:
                success = send_dm(user_id, message)
                if success:
                    sent_users.add(user_id)
                time.sleep(5)  # Delay between messages to avoid spam detection
        
        print("Waiting before next check...")
        time.sleep(60)  # Wait a minute before checking for new comments

if __name__ == "__main__":
    main()
