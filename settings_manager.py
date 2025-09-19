import os
import json
import logging

class SettingsManager:
    def __init__(self):
        self.settings_file = os.path.join(os.path.expanduser("~"), ".zestsyncsetting.json")
        self.default_settings = {
            "accuracy_mode": "fast"  # "fast" or "slow"
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            logging.info(f"Settings saved to {self.settings_file}")
        except Exception as e:
            logging.error(f"Error saving settings: {e}")
    
    def get_accuracy_mode(self):
        return self.settings.get("accuracy_mode", "fast")
    
    def set_accuracy_mode(self, mode):
        if mode in ["fast", "slow"]:
            self.settings["accuracy_mode"] = mode
            self.save_settings()
            logging.info(f"Accuracy mode set to: {mode}")
        else:
            logging.error(f"Invalid accuracy mode: {mode}")