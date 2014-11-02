import unittest
from mock import patch
import autohockey
import os

class TestAutoHockey(unittest.TestCase):

    def setUp(self):
        self.fake_token = 'faketoken'
        self.fake_apk = 'fake.apk'
        self.fake_ipa = 'fake.ipa'
        self.fake_dsym = 'fake.dsym'
        self.fake_not_present_apk = 'fake_not_present.apk'
        self.fake_not_present_ipa = 'fake_not_present.ipa'
        self.fake_not_present_dsym = 'fake_not_present.dsym'
        open(self.fake_apk, 'wb').write('hello')
        open(self.fake_ipa, 'wb').write('hello')
        open(self.fake_dsym, 'wb').write('hello')

    def tearDown(self):
        os.remove(self.fake_apk)
        os.remove(self.fake_ipa)
        os.remove(self.fake_dsym)

    def _get_request_parameters(self, build_file, api_token='', dsym='', notify=2, notes=''):
        return {
            'headers':{'X-HockeyAppToken': api_token},
            'data':{'notes': notes, 'dsym': dsym, 'notify': notify},
            'url':autohockey.UPLOAD_URL
        }

    @patch('autohockey.requests')
    def test_upload_is_called(self, mock_upload_requests):
        autohockey.upload(self.fake_apk, api_token=self.fake_token)
        params = self._get_request_parameters(self.fake_apk, api_token=self.fake_token)
        params_called = mock_upload_requests.post.call_args
        self.assertEqual(self.fake_apk, params_called[1]['files']['ipa'].name)
        del params_called[1]['files']
        mock_upload_requests.post.assert_called_with(**params)

    @patch('autohockey.requests')
    def test_raises_exception_if_build_file_not_present(self, mock_upload_requests):
        self.assertRaises(autohockey.AutoHockeyBadFile, autohockey.upload,
            self.fake_not_present_apk,
            api_token=self.fake_token)
        self.assertEqual(False, mock_upload_requests.post.called)

    @patch('autohockey.requests')
    def test_raises_exception_if_dsym_file_not_present(self, mock_upload_requests):
        self.assertRaises(autohockey.AutoHockeyBadFile, autohockey.upload,
            self.fake_ipa,
            dsym=self.fake_not_present_dsym,
            api_token=self.fake_token)
        self.assertEqual(False, mock_upload_requests.post.called)
