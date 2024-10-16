import os

def get_hotfix_version():
    result = os.popen('systeminfo').read()
 
    hotfixes = []
    collecting_hotfixes = False

    for line in result.splitlines():
        if "Hotfix(s):" in line:
            collecting_hotfixes = True
        
        if collecting_hotfixes and (line.startswith("KB") or "KB" in line):
            hotfixes.append(line.strip())

    return hotfixes

if __name__ == "__main__":
    hotfix_version = get_hotfix_version()
    
    if hotfix_version:
        print("Detailed Hotfix Information:")
        for hotfix in hotfix_version:
            print(f"Hotfix: {hotfix}")
    else:
        print("No hotfix information found.")
