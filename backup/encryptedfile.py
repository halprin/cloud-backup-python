import aws_encryption_sdk
from aws_encryption_sdk import KMSMasterKeyProvider
from botocore.session import Session


class EncryptedFile:

    ENCRYPTION_CONTEXT = {
        'context': 'encryption_context'
    }

    def __init__(self, path_to_encrypt, out_path, kms_key, aws_profile):
        self.path = path_to_encrypt
        self.out_path = out_path
        self.kms_key = kms_key
        self.aws_profile = aws_profile

    def encrypt(self):
        kms_key_provider = KMSMasterKeyProvider(key_ids=[self.kms_key],
                                                botocore_session=Session(profile=self.aws_profile))

        with open(self.path, 'rb') as plain_file, open(self.out_path, 'wb') as cipher_file:
            with aws_encryption_sdk.stream(mode='e', source=plain_file, key_provider=kms_key_provider,
                                           encryption_context=self.ENCRYPTION_CONTEXT,
                                           frame_length=1048576) as encryptor:
                for chunk in encryptor:
                    cipher_file.write(chunk)

    def decrypt(self):
        kms_key_provider = KMSMasterKeyProvider(key_ids=[self.kms_key],
                                                botocore_session=Session(profile=self.aws_profile))

        with open(self.out_path, 'rb') as cipher_file, open(self.path, 'wb') as plain_file:
            with aws_encryption_sdk.stream(mode='d', source=cipher_file, key_provider=kms_key_provider) as decryptor:
                encryption_context = decryptor.header.encryption_context
                if self._dictionary_is_subset(encryption_context, self.ENCRYPTION_CONTEXT) is False:
                    print("Decrypted context doesn't match original context! {}".format(encryption_context))
                    return
                for chunk in decryptor:
                    plain_file.write(chunk)

    def encrypted_path(self):
        return self.out_path

    @staticmethod
    def _dictionary_is_subset(superset, subset):
        is_subset = True
        for item in subset.items():
            key = item[0]
            if key not in superset or superset[key] != item[1]:
                is_subset = False
                break

        return is_subset

