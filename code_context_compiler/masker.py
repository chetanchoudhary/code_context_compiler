import re

def mask_sensitive_info(code):
    patterns = [
        r'password\s*=\s*["\'].*?["\']',
        r'api[_-]?key\s*=\s*["\'].*?["\']',
        r'secret\s*=\s*["\'].*?["\']',
        r'token\s*=\s*["\'].*?["\']',
        r'client[_-]?id\s*=\s*["\'].*?["\']',
        r'client[_-]?secret\s*=\s*["\'].*?["\']',
        r'access[_-]?token\s*=\s*["\'].*?["\']',
        r'refresh[_-]?token\s*=\s*["\'].*?["\']',
        r'private[_-]?key\s*=\s*["\'].*?["\']',
        r'public[_-]?key\s*=\s*["\'].*?["\']',
        r'aws[_-]?access[_-]?key[_-]?id\s*=\s*["\'].*?["\']',
        r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'].*?["\']',
        r'ssh[_-]?key\s*=\s*["\'].*?["\']',
        r'database[_-]?url\s*=\s*["\'].*?["\']',
        r'username\s*=\s*["\'].*?["\']'
    ]
    
    masked_code = code
    for pattern in patterns:
        masked_code = re.sub(pattern, '***MASKED***', masked_code)
    
    return masked_code