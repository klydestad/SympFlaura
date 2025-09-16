import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

print("=== DEBUGGING AUTHENTICATION ===\n")

# Test password hashing
print("1. Testing password hashing:")
passwords = ['sympflaura123']
try:
    # Try new API first
    hashed_passwords = stauth.Hasher(passwords).generate()
    print(f"Generated hash for 'sympflaura123': {hashed_passwords[0]}")
except:
    try:
        # Try alternative API
        hasher = stauth.Hasher(passwords)
        hashed_passwords = hasher.generate()
        print(f"Generated hash for 'sympflaura123': {hashed_passwords[0]}")
    except Exception as e:
        print(f"Error generating hash: {e}")
        # Manual bcrypt approach
        import bcrypt
        password = 'sympflaura123'.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        print(f"Generated hash for 'sympflaura123': {hashed.decode('utf-8')}")
        hashed_passwords = [hashed.decode('utf-8')]
print()

# Load and check current config
print("2. Current config.yaml contents:")
try:
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    
    print("Usernames found:")
    for username, details in config['credentials']['usernames'].items():
        print(f"  - {username}: {details['first_name']} {details['last_name']}")
        print(f"    Email: {details['email']}")
        print(f"    Password hash: {details['password']}")
        print(f"    Failed attempts: {details.get('failed_login_attempts', 0)}")
        print()
    
except Exception as e:
    print(f"Error loading config: {e}")

print("3. Testing if passwords match:")
for username, details in config['credentials']['usernames'].items():
    stored_hash = details['password']
    try:
        # Try different methods to check password
        is_valid = False
        try:
            is_valid = stauth.Hasher.check_pw('sympflaura123', stored_hash)
        except:
            # Alternative method using bcrypt directly
            import bcrypt
            is_valid = bcrypt.checkpw('sympflaura123'.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f"  {username}: Password 'sympflaura123' matches stored hash: {is_valid}")
    except Exception as e:
        print(f"  {username}: Error checking password: {e}")

print("\n4. Recommended test credentials:")
print("Username: jsmith")
print("Password: sympflaura123")
print("\nUsername: rbriggs") 
print("Password: sympflaura123")