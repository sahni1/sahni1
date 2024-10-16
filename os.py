import platform
import os

def get_os_info():
    os_info = {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'Architecture': platform.architecture()[0],
        'OS Uptime': os.popen('uptime').read() if os.name == 'posix' else 'Uptime command not available'
    }
    
    return os_info

if __name__ == '__main__':
    info = get_os_info()
    for key, value in info.items():
        print(f'{key}: {value}')
