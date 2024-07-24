import pytest
from code_context_compiler.masker import mask_sensitive_info, create_mask_function

@pytest.mark.parametrize("code, patterns, expected", [
    ('password = "secret"', [r'password\s*=\s*["\'].*?["\']'], 'password = "******"'),
    ('api_key = "12345"', [r'api[_-]?key\s*=\s*["\'].*?["\']'], 'api_key = "*****"'),
    ('normal_var = "value"', [r'password\s*=\s*["\'].*?["\']'], 'normal_var = "value"'),
])
def test_mask_sensitive_info_simple(code, patterns, expected):
    masked_code = mask_sensitive_info(code, patterns)
    assert masked_code == expected

def test_mask_sensitive_info_complex():
    code = '''
    password = "supersecret123"
    api_key = "abcdef1234567890"
    credit_card = "1234-5678-9012-3456"
    '''
    patterns = [
        r'password\s*=\s*["\'].*?["\']',
        {
            'pattern': r'api[_-]?key\s*=\s*["\'].*?["\']',
            'mask_char': '#',
            'preserve_length': False
        },
        {
            'pattern': r'\d{4}-\d{4}-\d{4}-\d{4}',
            'mask_char': 'X',
            'preserve_length': True
        }
    ]
    expected = '''
    password = "**************"
    api_key = "################"
    credit_card = "XXXXXXXXXXXXXXXXXXX"
    '''
    masked_code = mask_sensitive_info(code, patterns)
    assert masked_code.strip() == expected.strip()

# def test_create_mask_function():
#     mask_func = create_mask_function(mask_char='#', preserve_length=True)
#     assert mask_func(type('MockMatch', (), {'group': lambda: 'test = "value"'})()) == 'test = "#####"'

#     mask_func = create_mask_function(mask_char='*', preserve_length=False)
#     assert mask_func(type('MockMatch', (), {'group': lambda: 'test = "value"'})()) == 'test = "********"'
