import unittest
import gradio as gr
from daypack import DayPack
from daypack import DeviceManager

# Only to be run when an Android Device or Emulator is connected
class TestDayAndroidPack(unittest.TestCase):
    def setUp(self):
            # Create a simple Gradio interface for testing
            def echo(text):
                return text
            self.interface = gr.Interface(fn=echo, inputs="text", outputs="text")
            self.daypack = DayPack(self.interface)

    def testHello(self):
         self.daypack.launch()
         self.assertEqual(self.daypack.hosted_uri, self.interface.share_url)

if __name__ == '__main__':
    unittest.main()