import subprocess
import re

def get_dotnet_versions():
    net_versions = []
    registry_path = r"HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP"

    try:
        output = subprocess.check_output(['reg', 'query', registry_path, '/s', '/f', 'Version', '/t', 'REG_SZ'], shell=True).decode()
        
        version_dict = {}
        lines = output.splitlines()

        for line in lines:
            if "Version" in line:
                parts = line.split()
                if len(parts) > 1:
                    version = parts[-1]
                    key = re.sub(r"\\[^\\]+$", "", line).strip()
                    if key in version_dict:
                        version_dict[key].add(version)
                    else:
                        version_dict[key] = {version}
        
        for key, versions in version_dict.items():
            formatted_versions = ', '.join(sorted(versions))
            net_versions.append(f"{key}: {formatted_versions}")

    except subprocess.CalledProcessError as e:
        net_versions.append(f"Error retrieving .NET versions: {str(e)}")
    except Exception as e:
        net_versions.append(f"Unexpected error: {str(e)}")
    
    return net_versions

if __name__ == "__main__":
    versions = get_dotnet_versions()
    if versions:
        print("Installed .NET Versions:")
        for version in versions:
            print(version)
    else:
        print("No .NET versions found.")
