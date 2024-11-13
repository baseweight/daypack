import argparse
import gradio as gr
from gradio import Interface
from device import DeviceManager, Device

class DayPack:
    def __init__(self, interface):
        self.block = interface
        # This should probably be a singleton
        self.deviceManager = DeviceManager()

    # Pack builds the DayPack application
    # This is the meat and potatoes of the app, and this is where we store the model 
    # and point to the Gradio deployment.
    def pack(self):
        self.currentDevice.build(self.hosted_uri)
        return;

    # You need to supply your Hugging Face credential here
    def set_uri(self, uri):
        self.local = False
        self.hosted_uri = uri

    def set_on_device(self):
        self.local = True
        # The scheme is an easter egg only real ones will understand
        self.hosted_uri = "gap:gradio-local"

    # This installs the app package onto the device
    def install(self, deviceId):
        self.currentDevice = self.deviceManager.getDeviceById(deviceId)
        self.currentDevice.install()
        return
    
    def launch(self, deviceId=None):
        devices = self.devices()
        if not devices:
            raise Exception("No devices found. Please connect a device.")
        
        if deviceId is not None:
            self.currentDevice = self.deviceManager.getDeviceById(deviceId)
        else:
            self.currentDevice = devices[0]
        
        # Launch Gradio demo
        self.block.launch(share=True)
        
        # Set the URL in the mobile app
        self.set_uri(self.block.share_url)
        
        # Install and launch on device
        self.currentDevice.build(self.hosted_uri)
        self.currentDevice.install()
        self.currentDevice.launch()
        

    # This gets a list of currently installed devices
    # A DayPack can only have one device at at time installed.  We can have numerous daypacks 
    # but for starters we are only going to have one device setup.
    def devices(self):
        return self.deviceManager.devices()
    
    def getCurrentDevice(self):
        return self.currentDevice

    def add_model(self, filename):
        return

    def start(self):
        return
 
def main():
    parser = argparse.ArgumentParser(description="DayPack CLI")
    parser.add_argument("--install", action="store_true", help="Install the daypack on the device")
    parser.add_argument("--devices", action="store_true", help="List available devices")
    parser.add_argument("--add-model", type=str, help="Add a model file to the daypack")
    parser.add_argument("--start", action="store_true", help="Start the DayPack")

    args = parser.parse_args()

    if args.install:
        daypack.install()
    elif args.devices:
        daypack.devices()
    elif args.add_model:
        daypack.add_model(args.add_model)
    elif args.start:
        daypack.start()
    else:
        parser.print_help()