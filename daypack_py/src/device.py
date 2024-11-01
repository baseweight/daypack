import os
import xml.etree.ElementTree as ET
import tidevice
from ppadb.client import Client as AdbClient

ANDROID_PROJECT_PATH = ""
IOS_PROJECT_PATH = ""

class Device:
    def __init__(self, deviceType, deviceId):
        self.deviceType = deviceType
        self.deviceId = deviceId
        return
    
    def install(self, app_path):
        if self.deviceType == "Android":
            # Use the adb clinet to install an APK that we built
            self.adb_client.install(app_path)
        elif self.deviceType == "iOS":
            # Use tidevice to do the deployment of the compiled iOS application
            self.ios_device.install(app_path)
        return
    
    def set_android_launch_path(self, hosted_uri):
        # Path to the strings.xml file
        strings_xml_path = os.path.join(ANDROID_PROJECT_PATH, "res", "values", "strings.xml")

        # Parse the XML file
        tree = ET.parse(strings_xml_path)
        root = tree.getroot()

        # Find the launch_url string and update its value
        for string in root.findall('string'):
            if string.get('name') == 'launch_url':
                string.text = hosted_uri
                break

        # Write the changes back to the file
        tree.write(strings_xml_path, encoding="utf-8", xml_declaration=True)

        print(f"Updated launch_url to {hosted_uri} in {strings_xml_path}")

    def set_ios_launch_path(self, hosted_uri):
        config_path = os.path.join(IOS_PROJECT_PATH, "config.json")
        
        config = {
            "webviewUrl": hosted_uri
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        print(f"Updated webview URL to {hosted_uri} in {config_path}")        


    def build(self, hosted_uri):
        if self.deviceType == "Android":
            self.set_android_launch_path(hosted_uri)
        elif self.deviceType == "iOS":
            self.set_ios_launch_path(hosted_uri)

    
class DeviceManager:
    def __init__(self):
        self.ios_device = tidevice.Device()
        self.adb_client = AdbClient(host="127.0.0.1", port=5037)

    def get_devices(self):
        androids = self.adb_client.devices()
        #TODO: Figure out how to get a list of iOS devices from Python
        #TODO: Use our device 
        return androids