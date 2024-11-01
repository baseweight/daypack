import unittest
import gradio as gr
from daypack import DayPack
from daypack import DeviceManager

class TestDayPack(unittest.TestCase):
    def setUp(self):
        # Create a simple Gradio interface for testing
        def echo(text):
            return text
        self.interface = gr.Interface(fn=echo, inputs="text", outputs="text")
        self.daypack = DayPack(self.interface)

    def test_initialization(self):
        self.assertIsNotNone(self.daypack.block)
        self.assertIsNotNone(self.daypack.deviceManager)
        self.assertIsInstance(self.daypack.deviceManager, DeviceManager)

    def test_set_uri(self):
        test_uri = "https://huggingface.co/spaces/test/demo"
        self.daypack.set_uri(test_uri)
        self.assertEqual(self.daypack.hosted_uri, test_uri)
        self.assertFalse(self.daypack.local)

    def test_set_on_device(self):
        self.daypack.set_on_device()
        self.assertEqual(self.daypack.hosted_uri, "gap:gradio-local")
        self.assertTrue(self.daypack.local)

    def test_install(self):
        device_id = "test_device_id"
        self.daypack.install(device_id)
        self.assertIsNotNone(self.daypack.currentDevice)

    def test_devices(self):
        devices = self.daypack.devices()
        self.assertIsNotNone(devices)

    def test_get_current_device(self):
        device_id = "test_device_id"
        self.daypack.install(device_id)
        current_device = self.daypack.getCurrentDevice()
        self.assertIsNotNone(current_device)

if __name__ == '__main__':
    unittest.main()
