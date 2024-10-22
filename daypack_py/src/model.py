class Model:
    def __init__(self, path):
        self.data = None
        self.file_path = None
        self.load_from_json(file_path=path)
        

    def load_from_json(self, file_path):
        import json
        self.file_path = file_path
        try:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")

    # Attempt to load the file in the Python Interpreter
    # before running it on a device, because we might have garbage
    #        
    def is_model_valid(self):
        if self.model_type == "ANDROID":
            return True;
        elif self.model_type == "iOS":
            return True;
        else: 
            return False
