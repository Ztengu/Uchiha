import requests
import random
import time
import os
from colorama import Fore, init

# Init colorama
init(autoreset=True)

# Display banner
print("   __________          __        __   ")
print("  |__  /__  /  ____   / /_   ___/ /__ ")
print("    / /  / /   / __ \ / __ \ / _  / -_)")
print("   /_/  /_/   /_/ /_//_/ /_/ \_,_/\__/ ")
print("                                       ")
print("========= THE TANK CREW ===============")
print("Author: The Tank Crew")
print("Script: Discord Push Rank")
print("Telegram: @TheTankCrew")
print("Youtube: The Tank Crew")
print("===========================================")
print('WARNING: NOT FOR SALE / RESALE')
print("===========================================\n")

time.sleep(1)

# Input with validation
while True:
    channel_id = input("Enter Channel ID: ").strip()
    if channel_id and channel_id.isdigit():
        break
    print(Fore.RED + "❌ Channel ID must be a number!")

while True:
    try:
        delete_delay = int(input("Set Delete Message Delay (seconds): "))
        send_delay = int(input("Set Send Message Delay (seconds): "))
        break
    except ValueError:
        print(Fore.RED + "❌ Please enter valid numbers!")

time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')

# Load messages with validation
try:
    with open("messages.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f.readlines() if line.strip()]
    if not words:
        print(Fore.RED + "❌ messages.txt is empty!")
        exit()
except FileNotFoundError:
    print(Fore.RED + "❌ messages.txt not found!")
    print(Fore.YELLOW + "📝 Create messages.txt with your messages (one per line)")
    exit()

# Load token with validation
try:
    with open("token.txt", "r", encoding="utf-8") as f:
        token = f.readline().strip()
        if not token:
            print(Fore.RED + "❌ Token is empty in token.txt!")
            exit()
        # Validate token format
        if not token.startswith(('MT', 'mfa.', 'ND')):
            print(Fore.YELLOW + "⚠️ Token might be invalid! Make sure it's a valid Discord token.")
except FileNotFoundError:
    print(Fore.RED + "❌ token.txt not found!")
    print(Fore.YELLOW + "📝 Create token.txt and paste your Discord token inside")
    exit()

def test_token():
    """Test if token is valid"""
    headers = {'Authorization': token}
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        if r.status_code == 200:
            user_data = r.json()
            print(Fore.GREEN + f"✅ Token valid! Logged in as: {user_data.get('username')}#{user_data.get('discriminator')}")
            return True
        else:
            print(Fore.RED + f"❌ Invalid token! Status: {r.status_code}")
            if r.status_code == 401:
                print(Fore.YELLOW + "⚠️ Token may be expired or revoked!")
            return False
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Error testing token: {e}")
        return False

def test_channel():
    """Test if channel is valid and accessible"""
    headers = {'Authorization': token}
    try:
        r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers, timeout=10)
        if r.status_code == 200:
            channel_data = r.json()
            print(Fore.GREEN + f"✅ Channel valid! Name: {channel_data.get('name', 'Unknown')}")
            return True
        elif r.status_code == 404:
            print(Fore.RED + f"❌ Channel with ID {channel_id} not found!")
            return False
        elif r.status_code == 403:
            print(Fore.RED + f"❌ No access to channel {channel_id}!")
            print(Fore.YELLOW + "⚠️ Make sure your token has permission to send messages in this channel.")
            return False
        else:
            print(Fore.RED + f"❌ Error checking channel: {r.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Error: {e}")
        return False

# Test token and channel before starting
print("\n" + "="*50)
print("🔍 TESTING TOKEN & CHANNEL...")
print("="*50)

if not test_token():
    print(Fore.RED + "\n❌ Invalid token! Check token.txt")
    print("📝 How to get token:")
    print("1. Open Discord in browser")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Network tab and find a request to discord.com")
    print("4. Look for 'Authorization' header")
    print("5. Copy the token to token.txt")
    exit()

if not test_channel():
    print(Fore.RED + "\n❌ Invalid channel! Check:")
    print("1. Channel ID (use numeric ID, not channel name)")
    print("2. Token permissions in the channel/server")
    print("3. Make sure channel is not a private/voice channel")
    print("4. How to get ID: Settings > Advanced > Developer Mode > Copy ID")
    exit()

print("="*50)
print(Fore.GREEN + "✅ All tests passed! Starting script...\n")

def send_message():
    """Send message with error handling"""
    try:
        payload = {'content': random.choice(words)}
        headers = {'Authorization': token}
        
        r = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            data=payload,
            headers=headers,
            timeout=10
        )
        
        print(Fore.WHITE + "📤 Sent message: ")
        print(Fore.YELLOW + f"  {payload['content']}")
        
        if r.status_code == 201:
            print(Fore.GREEN + f"  ✅ Message sent! ID: {r.json().get('id')}")
            return r.json()
        elif r.status_code == 401:
            print(Fore.RED + "  ❌ Token expired! Stopping script...")
            print(Fore.YELLOW + "  📝 Update token in token.txt and restart")
            exit()
        elif r.status_code == 429:
            print(Fore.YELLOW + "  ⚠️ Rate limited! Waiting 5 seconds...")
            time.sleep(5)
            return None
        elif r.status_code == 403:
            print(Fore.RED + "  ❌ No permission to send messages in this channel!")
            return None
        else:
            print(Fore.RED + f"  ❌ Failed to send: {r.status_code}")
            print(f"  Response: {r.text[:200]}")  # Show first 200 chars of error
            return None
            
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"  ❌ Error sending: {e}")
        return None

def delete_last_message():
    """Delete the last message with error handling"""
    try:
        headers = {'Authorization': token}
        response = requests.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            params={'limit': 1},
            timeout=10
        )
        
        if response.status_code != 200:
            print(Fore.RED + f"  ❌ Failed to fetch messages: {response.status_code}")
            return False
            
        messages = response.json()
        if not messages:
            print(Fore.YELLOW + "  ⚠️ No messages to delete")
            return True
            
        message_id = messages[0]['id']
        
        # Check if message is from our token/user
        message_author_id = messages[0].get('author', {}).get('id')
        
        # Get current user ID
        user_response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if user_response.status_code == 200:
            current_user_id = user_response.json().get('id')
            if message_author_id != current_user_id:
                print(Fore.YELLOW + f"  ⚠️ Last message is not from our token, skipping delete")
                return True
        
        # Delete the message
        r = requests.delete(
            f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}",
            headers=headers,
            timeout=10
        )
        
        if r.status_code == 204:
            print(Fore.GREEN + f"  ✅ Message {message_id} deleted")
            return True
        elif r.status_code == 401:
            print(Fore.RED + "  ❌ Token expired!")
            exit()
        elif r.status_code == 403:
            print(Fore.YELLOW + "  ⚠️ No permission to delete messages!")
            return False
        else:
            print(Fore.RED + f"  ❌ Failed to delete: {r.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"  ❌ Error deleting: {e}")
        return False

# Main loop
counter = 0
print(Fore.CYAN + "🚀 Script started! Press CTRL+C to stop\n")

while True:
    try:
        counter += 1
        print(f"\n--- Loop #{counter} ---")
        
        # Send message
        result = send_message()
        
        if result:
            # Wait before deleting
            print(f"  ⏳ Waiting {delete_delay} seconds before delete...")
            time.sleep(delete_delay)
            
            # Delete last message
            delete_last_message()
        else:
            print(Fore.YELLOW + "  ⚠️ Skipping delete because message failed to send")
        
        # Wait before sending next message
        print(f"  ⏳ Waiting {send_delay} seconds before next message...")
        time.sleep(send_delay)
        
        # Clear terminal every 10 loops for cleanliness
        if counter % 10 == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.CYAN + f"🔄 Running... Loop #{counter}")
            print(Fore.CYAN + f"📊 Total messages sent: {counter}")
            print(Fore.CYAN + "🚀 Press CTRL+C to stop\n")
            
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⏹️ Script stopped by user!")
        print(Fore.GREEN + f"📊 Total messages sent: {counter}")
        break
    except Exception as e:
        print(Fore.RED + f"❌ Unexpected error: {e}")
        print(Fore.YELLOW + "⏳ Waiting 5 seconds before continuing...")
        time.sleep(5)