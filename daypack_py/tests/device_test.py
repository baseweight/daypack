import unittest
from device import Device, DeviceManager

class TestDevice(unittest.TestCase):
    def setUp(self):
        self.device = Device()

    def test_initialization(self):
        self.assertIsNotNone(self.device)
        self.assertEqual(self.device.id, "")
        self.assertEqual(self.device.name, "")
        self.assertEqual(self.device.type, "")
        self.assertEqual(self.device.status, "disconnected")

    def test_set_device_info(self):
        test_id = "device123"
        test_name = "Test Device"
        test_type = "ios"
        
        self.device.set_device_info(test_id, test_name, test_type)
        
        self.assertEqual(self.device.id, test_id)
        self.assertEqual(self.device.name, test_name)
        self.assertEqual(self.device.type, test_type)

    def test_connect_disconnect(self):
        self.device.connect()
        self.assertEqual(self.device.status, "connected")
        
        self.device.disconnect()
        self.assertEqual(self.device.status, "disconnected")

class TestDeviceManager(unittest.TestCase):
    def setUp(self):
        self.device_manager = DeviceManager()

    def test_initialization(self):
        self.assertIsNotNone(self.device_manager)
        self.assertEqual(len(self.device_manager.devices), 0)

    def test_add_remove_device(self):
        test_device = Device()
        test_device.set_device_info("test123", "Test Device", "ios")
        
        # Test adding device
        self.device_manager.add_device(test_device)
        self.assertEqual(len(self.device_manager.devices), 1)
        
        # Test removing device
        self.device_manager.remove_device(test_device.id)
        self.assertEqual(len(self.device_manager.devices), 0)

    def test_get_device(self):
        test_device = Device()
        test_device.set_device_info("test123", "Test Device", "ios")
        self.device_manager.add_device(test_device)
        
        retrieved_device = self.device_manager.get_device("test123")
        self.assertIsNotNone(retrieved_device)
        self.assertEqual(retrieved_device.id, "test123")
        
        # Test getting non-existent device
        non_existent = self.device_manager.get_device("fake_id")
        self.assertIsNone(non_existent)

    def test_get_all_devices(self):
        test_device1 = Device()
        test_device1.set_device_info("test1", "Test Device 1", "ios")
        test_device2 = Device()
        test_device2.set_device_info("test2", "Test Device 2", "ios")
        
        self.device_manager.add_device(test_device1)
        self.device_manager.add_device(test_device2)
        
        devices = self.device_manager.get_all_devices()
        self.assertEqual(len(devices), 2)

if __name__ == '__main__':
    unittest.main()
