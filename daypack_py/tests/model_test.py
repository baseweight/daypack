import unittest
from model import Model

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = Model()

    def test_initialization(self):
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.name, "")
        self.assertEqual(self.model.path, "")
        self.assertEqual(self.model.type, "")

    def test_set_model_info(self):
        test_name = "test_model"
        test_path = "/path/to/model"
        test_type = "coreml"
        
        self.model.set_model_info(test_name, test_path, test_type)
        
        self.assertEqual(self.model.name, test_name)
        self.assertEqual(self.model.path, test_path)
        self.assertEqual(self.model.type, test_type)

    def test_validate_model(self):
        # Test invalid model
        self.model.set_model_info("", "", "")
        self.assertFalse(self.model.validate())

        # Test valid model
        self.model.set_model_info("test", "/path", "coreml")
        self.assertTrue(self.model.validate())

    def test_supported_model_types(self):
        supported_types = self.model.get_supported_types()
        self.assertIsInstance(supported_types, list)
        self.assertIn("coreml", supported_types)

if __name__ == '__main__':
    unittest.main()
