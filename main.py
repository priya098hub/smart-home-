import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

# -------------------- Base Device Class --------------------
class Device:
    """Base class for all smart devices"""
    def __init__(self, name: str, device_type: str):
        self.name = name
        self.device_type = device_type
        self.switched_on = False
    
    def toggle_switch(self) -> None:
        self.switched_on = not self.switched_on
    
    def get_status(self) -> str:
        raise NotImplementedError
    
    def __str__(self) -> str:
        return f"{self.device_type} - {self.name}"

# -------------------- Smart Plug Class (Task 1) --------------------
class SmartPlug(Device):
    def __init__(self, name: str, consumption_rate: int = 45):
        super().__init__(name, "SmartPlug")
        self._consumption_rate = 45  # Default value
        self.consumption_rate = consumption_rate  # Use property setter
    
    @property
    def consumption_rate(self):
        return self._consumption_rate
    
    @consumption_rate.setter
    def consumption_rate(self, value):
        if 0 <= value <= 150:
            self._consumption_rate = value
        else:
            raise ValueError("Consumption rate must be between 0-150 watts")
    
    def get_status(self):
        state = "ON" if self.switched_on else "OFF"
        return f"{self.device_type}: {self.name}\nState: {state}\nConsumption: {self.consumption_rate}W"
    
    def __str__(self):
        state = "on" if self.switched_on else "off"
        return f"{self.device_type} is {state} with consumption rate of {self.consumption_rate}W"

# -------------------- Custom Devices (Task 2) --------------------
class SmartLight(Device):
    def __init__(self, name: str, brightness: int = 50):
        super().__init__(name, "SmartLight")
        self._brightness = 50
        self.brightness = brightness  # Use property setter
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        if 1 <= value <= 100:
            self._brightness = value
        else:
            raise ValueError("Brightness must be between 1-100%")
    
    def get_status(self):
        state = "ON" if self.switched_on else "OFF"
        return f"{self.device_type}: {self.name}\nState: {state}\nBrightness: {self.brightness}%"

class SmartFridge(Device):
    VALID_TEMPS = {1, 3, 5}
    
    def __init__(self, name: str, temperature: int = 3):
        super().__init__(name, "SmartFridge")
        self._temperature = 3
        self.temperature = temperature  # Use property setter
    
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        if value in self.VALID_TEMPS:
            self._temperature = value
        else:
            raise ValueError("Temperature must be 1, 3, or 5°C")
    
    def get_status(self):
        state = "ON" if self.switched_on else "OFF"
        return f"{self.device_type}: {self.name}\nState: {state}\nTemperature: {self.temperature}°C"

# -------------------- Smart Home Manager (Task 3) --------------------
class SmartHome:
    def __init__(self, max_devices=10):
        self.devices = []
        self.max_devices = max_devices
    
    def add_device(self, device: Device):
        if len(self.devices) < self.max_devices:
            self.devices.append(device)
        else:
            raise ValueError("Maximum device limit reached")
    
    def remove_device(self, index: int):
        if 0 <= index < len(self.devices):
            del self.devices[index]
        else:
            raise IndexError("Invalid device index")
    
    def toggle_device(self, index: int):
        if 0 <= index < len(self.devices):
            self.devices[index].toggle_switch()
    
    def switch_all_on(self):
        for device in self.devices:
            device.switched_on = True
    
    def switch_all_off(self):
        for device in self.devices:
            device.switched_on = False
    
    def __str__(self):
        return f"SmartHome with {len(self.devices)} device(s):\n" + "\n".join(
            f"{i+1}- {device}" for i, device in enumerate(self.devices))

# -------------------- GUI Application (Tasks 4 & 5) --------------------
class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Home Controller")
        self.geometry("800x600")
        self.smart_home = SmartHome()
        
        # Add default devices
        self.smart_home.add_device(SmartPlug("Kitchen Plug", 45))
        self.smart_home.add_device(SmartLight("Living Room Light"))
        self.smart_home.add_device(SmartFridge("Main Fridge"))
        
        self._create_widgets()
        self._update_device_list()
    
    def _create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Device list
        self.device_tree = ttk.Treeview(main_frame, columns=("status"), show="tree")
        self.device_tree.heading("#0", text="Devices")
        self.device_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        ttk.Button(control_frame, text="Toggle Device", command=self._toggle_device).pack(pady=5)
        ttk.Button(control_frame, text="Add Device", command=self._add_device).pack(pady=5)
        ttk.Button(control_frame, text="Remove Device", command=self._remove_device).pack(pady=5)
        ttk.Button(control_frame, text="All ON", command=lambda: self._toggle_all(True)).pack(pady=5)
        ttk.Button(control_frame, text="All OFF", command=lambda: self._toggle_all(False)).pack(pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(self, text="Ready")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _update_device_list(self):
        self.device_tree.delete(*self.device_tree.get_children())
        for idx, device in enumerate(self.smart_home.devices):
            status = "ON" if device.switched_on else "OFF"
            self.device_tree.insert("", "end", iid=str(idx), 
                                  text=f"{device.name} ({device.device_type})",
                                  values=(status,))
    
    def _toggle_device(self):
        selection = self.device_tree.selection()
        if selection:
            index = int(selection[0])
            self.smart_home.toggle_device(index)
            self._update_device_list()
    
    def _add_device(self):
        # Implementation for adding new devices
        pass
    
    def _remove_device(self):
        selection = self.device_tree.selection()
        if selection:
            index = int(selection[0])
            self.smart_home.remove_device(index)
            self._update_device_list()
    
    def _toggle_all(self, state: bool):
        if state:
            self.smart_home.switch_all_on()
        else:
            self.smart_home.switch_all_off()
        self._update_device_list()

# -------------------- Testing Functions --------------------
def test_smart_plug():
    try:
        plug = SmartPlug("Test Plug", 45)
        print("Initial state:", plug)
        
        plug.toggle_switch()
        print("After toggle:", plug)
        
        plug.consumption_rate = 75
        print("After update:", plug)
        
    except Exception as e:
        print("Error:", str(e))

def test_custom_device():
    try:
        light = SmartLight("Test Light")
        print("Light status:", light.get_status())
        
        fridge = SmartFridge("Test Fridge")
        print("Fridge status:", fridge.get_status())
        
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    # Run tests
    print("=== Testing SmartPlug ===")
    test_smart_plug()
    
    print("\n=== Testing Custom Devices ===")
    test_custom_device()
    
    # Run GUI
    app = SmartHomeApp()
    app.mainloop()
