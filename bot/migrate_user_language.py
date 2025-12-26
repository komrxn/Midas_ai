"""Migration script to add language field to existing users."""
import json
from pathlib import Path

def migrate_users():
    """Add default language field to users who don't have it."""
    users_file = Path("bot/data/users.json")
    
    if not users_file.exists():
        print("No users.json file found")
        return
    
    with open(users_file, 'r') as f:
        users = json.load(f)
    
    modified = False
    for user_id, user_data in users.items():
        if 'language' not in user_data:
            # Set default language to Russian for existing users 
            # (since the bot seems to be used in Russian-speaking context)
            user_data['language'] = 'ru'
            modified = True
            print(f"Added language 'ru' for user {user_id}")
    
    if modified:
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2, default=str)
        print(f"\n✅ Migration complete! Updated {len([u for u in users.values() if 'language' in u])} users")
    else:
        print("No migration needed - all users already have language field")

if __name__ == "__main__":
    migrate_users()
