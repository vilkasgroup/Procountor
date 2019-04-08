import unittest
import tempfile
import os
from tests import TestClient


class TestClientAttachment(TestClient):

    # Need for testing get attachment
    test_attachment_id = None
    # Need for testing attachment post and delete
    test_file_name = None
    test_reference_type = None
    test_reference_id = None

    def __init__(self, *args, **kwargs):
        super(TestClientAttachment, self).__init__(*args, **kwargs)
        self.__class__.test_attachment_id = os.getenv('PROCOUNTOR_ATTACHMENT_ID', None)
        self.__class__.test_file_name = os.getenv('PROCOUNTOR_ATTACHMENT_FILE_NAME', None)
        self.__class__.test_reference_type = os.getenv('PROCOUNTOR_ATTACHMENT_REFERENCE_TYPE', None)
        self.__class__.test_reference_id = os.getenv('PROCOUNTOR_ATTACHMENT_REFERENCE_ID', None)

    def test_get_001_attachment(self):
        if self.__class__.test_attachment_id:
            response = self.client.get_attachment(self.__class__.test_attachment_id)
            self.assertEqual(response['status'], 200)

    def test_post_002_attachment(self):
        if self.__class__.test_file_name and self.__class__.test_reference_type and self.__class__.test_reference_id:
            f = tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.txt', prefix='test_')
            f.write(b"Temp file - Procountor test")
            f.close()

            meta = {
                "name": self.__class__.test_file_name,
                "referenceType": self.__class__.test_reference_type,
                "referenceId": self.__class__.test_reference_id,
            }

            response = self.client.post_attachment(meta, f.name)

            self.assertEqual(response['status'], 200)
            attachmentId = response['content']['id']

            os.unlink(f.name)

            responseDelete = self.client.delete_attachment(attachmentId)
            self.assertEqual(responseDelete['status'], 200)

if __name__ == '__main__':
    unittest.main()