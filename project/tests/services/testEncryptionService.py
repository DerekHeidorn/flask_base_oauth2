
from project.tests.services.baseTest import BaseTest
from project.app.services import encryptionService


class EncryptionServiceTestCase(BaseTest):

    def test_encrypt_and_decrypt_string(self):
        print("running test_encrypt_and_decrypt_string...")

        test_string = "This is a test string"

        encrypted_string = encryptionService.encrypt_string(test_string)
        print("encrypted_string=" + str(encrypted_string))
        self.assertNotEqual(test_string, encrypted_string)

        decrypted_string = encryptionService.decrypt_string(encrypted_string)
        print("decrypted_string=" + str(decrypted_string))
        self.assertEqual(test_string, decrypted_string)

    def test_encrypt_and_decrypt_with_base64_string(self):
        print("running test_encrypt_and_decrypt_with_base64_string...")

        test_string = "This is a test string2"

        encrypted_string = encryptionService.encrypt_string_with_base64(test_string)
        print("encrypted_string=" + str(encrypted_string))
        self.assertNotEqual(test_string, encrypted_string)

        decrypted_string = encryptionService.decrypt_string_with_base64(encrypted_string)
        print("decrypted_string=" + str(decrypted_string))
        self.assertEqual(test_string, decrypted_string)

    def test_encrypt_and_decrypt_dictionary(self):
        print("running test_encrypt_and_decrypt_dictionary...")

        test_dictionary = {"abc": "123", "foo": "bar", "idea": "find yourself"}

        encrypted_string = encryptionService.encrypt_dictionary(test_dictionary)
        print("encrypted_string=" + str(encrypted_string))

        decrypted_dictionary = encryptionService.decrypt_dictionary(encrypted_string)
        print("decrypted_string=" + str(decrypted_dictionary))
        self.assertEqual(str(test_dictionary), str(decrypted_dictionary))

    def test_encrypt_and_decrypt_with_base64_dictionary(self):
        print("running test_encrypt_and_decrypt_with_base64_dictionary...")

        test_dictionary = {"abc": "123", "foo": "bar", "idea": "find yourself"}

        encrypted_string = encryptionService.encrypt_dictionary_with_base64(test_dictionary)
        print("encrypted_string=" + str(encrypted_string))

        decrypted_dictionary = encryptionService.decrypt_dictionary_with_base64(encrypted_string)
        print("decrypted_string=" + str(decrypted_dictionary))
        self.assertEqual(str(test_dictionary), str(decrypted_dictionary))
