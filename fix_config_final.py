import yaml
import bcrypt

# Generate fresh password hashes using bcrypt directly
password = 'sympflaura123'
hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
hash2 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"Generated hash 1: {hash1}")
print(f"Generated hash 2: {hash2}")

# Create new config with correct hashes
config = {
    'credentials': {
        'usernames': {
            'jsmith': {
                'email': 'jsmith@gmail.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'password': hash1,  # Fresh correct hash
                'roles': ['admin', 'editor', 'viewer'],
                'failed_login_attempts': 0,  # Reset failed attempts
                'logged_in': False
            },
            'rbriggs': {
                'email': 'rbriggs@gmail.com',
                'first_name': 'Rebecca',
                'last_name': 'Briggs', 
                'password': hash2,  # Fresh correct hash
                'roles': ['viewer'],
                'failed_login_attempts': 0,  # Reset failed attempts  
                'logged_in': False
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'sympflaura_secret_key_123',
        'name': 'sympflaura_auth_cookie'
    }
}

# Backup old config
import shutil
shutil.copy('config.yaml', 'config_backup.yaml')
print("✅ Backed up old config to config_backup.yaml")

# Save new config
with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

print("✅ Created new config.yaml with correct password hashes!")
print()
print("Now you can login with:")
print("  Username: jsmith")
print("  Password: sympflaura123")
print()
print("  Username: rbriggs") 
print("  Password: sympflaura123")
print()
print("Failed login attempts have been reset to 0 for both users.")

# Verify the new hashes work
print("\n=== VERIFICATION ===")
for username, details in config['credentials']['usernames'].items():
    stored_hash = details['password']
    is_valid = bcrypt.checkpw('sympflaura123'.encode('utf-8'), stored_hash.encode('utf-8'))
    print(f"✅ {username}: Password 'sympflaura123' matches: {is_valid}")