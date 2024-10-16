import requests

def search_cve_by_kb(kb_id):
    nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {
        'apiKey': '0d48c86d-1450-4200-b0b6-0ea0989065e2'  
    }

    params = {
        'keywordSearch': kb_id,
        'resultsPerPage': 5,
        'startIndex': 0
    }

    try:
        response = requests.get(nvd_url, params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response URL: {response.url}")
        print(f"Raw Response:\n{response.text}") 
        response.raise_for_status()  
        cve_data = response.json() 
        
        # Correct the path to access the vulnerabilities
        return cve_data.get('vulnerabilities', [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CVE data: {e}")
        return []

def display_cves(cve_list):
    if not cve_list:
        print("No CVEs found.")
        return

    for i, cve in enumerate(cve_list):
        cve_id = cve.get('cve', {}).get('id', 'Unknown')
        description = cve.get('cve', {}).get('descriptions', [{}])[0].get('value', 'No description available')
        
        print(f"CVE-{i+1}: {cve_id}")
        print(f"Description: {description}")
        print("------------------------------------------------------")

if __name__ == "__main__":
    kb_id = input("Enter the keyword ID: ")
    print(f"Searching for CVEs related to: {kb_id}")
    
    cve_list = search_cve_by_kb(kb_id)
    display_cves(cve_list)