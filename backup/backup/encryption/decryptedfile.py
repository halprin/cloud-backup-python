import aws_encryption_sdk
from aws_encryption_sdk import KMSMasterKeyProvider
from botocore.session import Session


class DecryptedFile:
    def __init__(self, path_to_decrypt, out_path, kms_key, aws_profile, encryption_context='encryption_context'):
        self.path = path_to_decrypt
        self.out_path = out_path
        self.kms_key = kms_key
        self.encryption_context = {
            'context': encryption_context if encryption_context is not None else 'encryption_context'}
        self.aws_profile = aws_profile

    def decrypt(self):
        kms_key_provider = KMSMasterKeyProvider(key_ids=[self.kms_key],
                                                botocore_session=Session(profile=self.aws_profile))

        with open(self.path, 'rb') as cipher_file, open(self.out_path, 'wb') as plain_file:
            with aws_encryption_sdk.stream(mode='d', source=cipher_file, key_provider=kms_key_provider) as decryptor:
                encrypted_context = decryptor.header.encryption_context
                if self._dictionary_is_subset(encrypted_context, self.encryption_context) is False:
                    print("Decrypted context doesn't match original context! {}".format(encrypted_context))
                    return
                for chunk in decryptor:
                    plain_file.write(chunk)

    def decrypted_path(self):
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

