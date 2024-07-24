import re
from typing import Dict, List, Union


def create_mask_function(
    mask_char: str = "*", preserve_length: bool = True
) -> callable:
    def mask_func(match: re.Match) -> str:
        value = match.group()
        if "=" in value:
            # Split the string at '=' and mask only the right side
            left, right = value.split("=", 1)
            masked_right = mask_char * (len(right.strip()) - 2)  # -2 for the quotes
            return f'{left}= "{masked_right}"'
        if preserve_length:
            return mask_char * len(value)
        return mask_char * 8  # Default masked length

    return mask_func


def mask_sensitive_info(
    code: str, patterns: List[Union[str, Dict[str, Union[str, bool]]]]
) -> str:
    for pattern in patterns:
        if isinstance(pattern, str):
            mask_func = create_mask_function()
            code = re.sub(pattern, mask_func, code)
        elif isinstance(pattern, dict):
            mask_char = pattern.get("mask_char", "*")
            preserve_length = pattern.get("preserve_length", True)
            mask_func = create_mask_function(mask_char, preserve_length)
            code = re.sub(pattern["pattern"], mask_func, code)
    return code


# Example usage
if __name__ == "__main__":
    test_code = """
    password = "supersecret123"
    api_key = "abcdef1234567890"
    credit_card = "1234-5678-9012-3456"
    """
    test_patterns = [
        r'password\s*=\s*["\'].*?["\']',
        {
            "pattern": r'api[_-]?key\s*=\s*["\'].*?["\']',
            "mask_char": "#",
            "preserve_length": False,
        },
        {
            "pattern": r"\d{4}-\d{4}-\d{4}-\d{4}",
            "mask_char": "X",
            "preserve_length": True,
        },
    ]
    print(mask_sensitive_info(test_code, test_patterns))
