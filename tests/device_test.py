import unittest
from daypack import Device, DeviceManager

class TestDevice(unittest.TestCase):
    def setUp(self):
        self.device = Device('Android', 'emualtor-5554')

    def test_initialization(self):
        device_id = "test123"
        device_type = "Android"
        device = Device(device_type, device_id)
        self.assertEqual(device.deviceId, device_id)
        self.assertEqual(device.deviceType, device_type)

    def test_android_project_setup(self):
        device = Device("Android", "test123")
        device.setup_android_project()
        self.assertTrue(device.ANDROID_PROJECT_PATH.startswith("/tmp"))

    def test_ios_project_setup(self):
        device = Device("iOS", "test123") 
        device.setup_ios_project()
        self.assertTrue(device.IOS_PROJECT_PATH.startswith("/tmp"))

    def test_set_android_launch_path(self):
        device = Device("Android", "test123")
        device.setup_android_project()
        test_uri = "https://test.com"
        device.set_android_launch_path(test_uri)
        # Verify strings.xml was updated
        import xml.etree.ElementTree as ET
        strings_xml = os.path.join(device.ANDROID_PROJECT_PATH, "res", "values", "strings.xml")
        tree = ET.parse(strings_xml)
        root = tree.getroot()
        launch_url = root.find("string[@name='launch_url']").text
        self.assertEqual(launch_url, test_uri)

    def test_set_ios_launch_path(self):
        device = Device("iOS", "test123")
        device.setup_ios_project() 
        test_uri = "https://test.com"
        device.set_ios_launch_path(test_uri)
        # Verify config.json was updated
        import json
        config_path = os.path.join(device.IOS_PROJECT_PATH, "config.json")
        with open(config_path) as f:
            config = json.load(f)
        self.assertEqual(config["webviewUrl"], test_uri)

    def test_build(self):
        device = Device("Android", "test123")
        test_uri = "https://test.com"
        device.build(test_uri)
        # Verify Android project was setup and launch path set
        self.assertTrue(device.ANDROID_PROJECT_PATH.startswith("/tmp"))
        import xml.etree.ElementTree as ET
        strings_xml = os.path.join(device.ANDROID_PROJECT_PATH, "res", "values", "strings.xml") 
        tree = ET.parse(strings_xml)
        root = tree.getroot()
        launch_url = root.find("string[@name='launch_url']").text
        self.assertEqual(launch_url, test_uri)


class TestDeviceManager(unittest.TestCase):
    def setUp(self):
        self.device_manager = DeviceManager()

    def test_initialization(self):
        self.assertIsNotNone(self.device_manager)

    def test_devices_empty(self):
        devices = self.device_manager.devices()
        self.assertEqual(len(devices), 0)


if __name__ == '__main__':
    unittest.main()
