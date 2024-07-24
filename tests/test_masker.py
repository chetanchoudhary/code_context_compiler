import pytest
from code_context_compiler.masker import mask_sensitive_info

@pytest.mark.parametrize("code, expected", [
    ('password = "secret"', 'password = "***MASKED***"'),
    ('api_key = "12345"', 'api_key = "***MASKED***"'),
    ('secret = "mysecret"', 'secret = "***MASKED***"'),
    ('token = "abcd1234"', 'token = "***MASKED***"'),
    ('client_id = "clientid123"', 'client_id = "***MASKED***"'),
    ('client_secret = "clientsecret456"', 'client_secret = "***MASKED***"'),
    ('access_token = "accesstoken789"', 'access_token = "***MASKED***"'),
    ('refresh_token = "refreshtoken012"', 'refresh_token = "***MASKED***"'),
    ('private_key = "privatekey345"', 'private_key = "***MASKED***"'),
    ('public_key = "publickey678"', 'public_key = "***MASKED***"'),
    ('aws_access_key_id = "awsaccesskeyid"', 'aws_access_key_id = "***MASKED***"'),
    ('aws_secret_access_key = "awssecretaccesskey"', 'aws_secret_access_key = "***MASKED***"'),
    ('ssh_key = "sshkey"', 'ssh_key = "***MASKED***"'),
    ('database_url = "databaseurl"', 'database_url = "***MASKED***"'),
    ('username = "user123"', 'username = "***MASKED***"')
])
def test_mask_sensitive_info(code, expected):
    masked_code = mask_sensitive_info(code)
    assert masked_code == expected