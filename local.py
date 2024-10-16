import subprocess
import re

def get_local_groups():
    try:
        result = subprocess.run(['net', 'localgroup'], capture_output=True, text=True, check=True)
        groups = result.stdout.splitlines()
        return [group.strip() for group in groups[4:] if group.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving local groups: {e}")
        return []

def get_non_empty_groups():
    groups = get_local_groups()
    non_empty_groups = {}
    for group in groups:
        try:
            result = subprocess.run(['net', 'localgroup', group], capture_output=True, text=True, check=True)
            members = result.stdout.splitlines()
            members = [member.strip() for member in members[4:] if member.strip()]
            if members:
                non_empty_groups[group] = members
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving members for group {group}: {e}")
    return non_empty_groups

def get_user_accounts():
    try:
        result = subprocess.run(['net', 'user'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()
        user_data = ' '.join(output_lines[3:-2])
        user_accounts = re.split(r'\s{2,}', user_data)
        user_accounts = [user for user in user_accounts if user and '---' not in user]
        return user_accounts
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving user accounts: {e}")
        return []

def get_user_status(user):
    try:
        result = subprocess.run(['net', 'user', user], capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if "Account active" in line:
                return "Active" if "Yes" in line else "Disabled"
        return "Unknown"
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving status for user {user}: {e}")
        return "Error"

def get_users_with_status():
    users = get_user_accounts()
    users_status = {}
    for user in users:
        status = get_user_status(user)
        users_status[user] = status
    return users_status

if __name__ == "__main__":
    print("Local Groups:")
    local_groups = get_local_groups()
    print(local_groups)

    print("\nNon-empty Groups and their Members:")
    non_empty_groups = get_non_empty_groups()
    for group, members in non_empty_groups.items():
        print(f"{group}: {', '.join(members)}")

    print("\nUsers and their Status:")
    users_status = get_users_with_status()
    for user, status in users_status.items():
        print(f"User: {user}, Status: {status}")
 