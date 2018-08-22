from sflvault.encryption.base import Encryption

def test_encryption_base_class():
    def create_mock_config():
        return {'test': 'test'}

    encryption = Encryption(create_mock_config)
    assert(encryption is not None)
