import os
import xml.etree.ElementTree as ET
import json
import tidevice
import subprocess
import shutil
import tempfile
from importlib.resources import files
from ppadb.client import Client as AdbClient

class Device:

    # Update the default paths to use package resources
    ANDROID_PROJECT_PATH = str(files('daypack').joinpath('templates/android'))
    IOS_PROJECT_PATH = str(files('daypack').joinpath('templates/ios'))

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
        strings_xml_path = os.path.join(self.ANDROID_PROJECT_PATH, "res", "values", "strings.xml")

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
        config_path = os.path.join(self.IOS_PROJECT_PATH, "config.json")
        
        config = {
            "webviewUrl": hosted_uri
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f)

        
        print(f"Updated webview URL to {hosted_uri} in {config_path}")        
 
    def setup_android_project(self):
        # Create a temporary directory for the Android project
        temp_dir = tempfile.mkdtemp()

        # Copy Android template project to temp directory
        shutil.copytree(self.ANDROID_PROJECT_PATH, temp_dir, dirs_exist_ok=True)
        
        # Update project path to use temp directory
        self.ANDROID_PROJECT_PATH = temp_dir
        
        print(f"Copied Android template project to {temp_dir}")

        return
    
    def setup_ios_project(self):
        # Create a temporary directory for the iOS project
        temp_dir = tempfile.mkdtemp()

        # Copy iOS template project to temp directory
        shutil.copytree(self.IOS_PROJECT_PATH, temp_dir, dirs_exist_ok=True)
        
        # Update project path to use temp directory
        self.IOS_PROJECT_PATH = temp_dir
        
        print(f"Copied iOS template project to {temp_dir}")
        return

    def build(self, hosted_uri):
        if self.deviceType == "Android":
            self.setup_android_project()
            self.set_android_launch_path(hosted_uri)
        elif self.deviceType == "iOS":
            self.set_ios_project()
            self.set_ios_launch_path(hosted_uri)

    def install(self):
        if self.deviceType == "Android":
            # Build the Android APK
            android_build_cmd = f"cd {self.ANDROID_PROJECT_PATH} && ./gradlew assembleDebug"
            subprocess.run(android_build_cmd, shell=True, check=True)

            # Get path to built APK
            apk_path = os.path.join(self.ANDROID_PROJECT_PATH, "app", "build", "outputs", "apk", "debug", "app-debug.apk")

            # Install the APK using ADB
            self.adb_client.install(apk_path)
        elif self.deviceType == "iOS":
            # Build the iOS IPA
            ios_build_cmd = f"cd {self.IOS_PROJECT_PATH} && xcodebuild -scheme DayPack -configuration Debug -derivedDataPath build"
            subprocess.run(ios_build_cmd, shell=True, check=True)

            # Get path to built IPA
            app_path = os.path.join(self.IOS_PROJECT_PATH, "build", "Build", "Products", "Debug-iphoneos", "DayPack.app")

            # Install the app using tidevice
            self.ios_device.app_install(app_path)

    
class DeviceManager:
    def __init__(self):
        self.ios_device = tidevice.Device()
        self.adb_client = AdbClient(host="127.0.0.1", port=5037)

    def get_devices(self):
        androids = self.adb_client.devices()
        #TODO: Figure out how to get a list of iOS devices from Python
        ios_devices = []
        try:
            # Get list of all connected iOS devices
            for device in tidevice.Usbmux().devices():
                ios_devices.append(device)
        except Exception as e:
            print(f"Error getting iOS devices: {e}")
        devices = []
        
        # Add Android devices
        for android_device in androids:
            device = Device()
            device.set_device_info(
                android_device.serial,
                f"Android Device ({android_device.serial})", 
                "Android"
            )
            devices.append(device)

        # Add iOS devices  
        for ios_device in ios_devices:
            device = Device()
            device.set_device_info(
                ios_device.udid,
                f"iOS Device ({ios_device.udid})",
                "iOS"
            )
            devices.append(device)
        return devices