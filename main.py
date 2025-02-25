import tkinter as tk
from tkinter import messagebox

# SmartPlug class
class SmartPlug:
    def __init__(self, name):
        self.name = name
        self.is_on = False
        self.consumption = 0
    
    def toggle(self):
        self.is_on = not self.is_on
        self.consumption = 0 if not self.is_on else 150
    
    def __str__(self):
        return f"{self.name} - {'ON' if self.is_on else 'OFF'} - {self.consumption}W"

# Custom Device Classes
class SmartLight(SmartPlug):
    def __init__(self, name, brightness=50):
        super().__init__(name)
        self.brightness = brightness
    
    def set_brightness(self, level):
        if 0 <= level <= 100:
            self.brightness = level
    
    def __str__(self):
        return f"{self.name} - {'ON' if self.is_on else 'OFF'} - Brightness: {self.brightness}%"

class SmartFridge(SmartPlug):
    def __init__(self, name, temperature=4):
        super().__init__(name)
        self.temperature = temperature
    
    def set_temperature(self, temp):
        if -10 <= temp <= 10:
            self.temperature = temp
    
    def __str__(self):
        return f"{self.name} - {'ON' if self.is_on else 'OFF'} - Temperature: {self.temperature}°C"

# SmartHome class
class SmartHome:
    def __init__(self):
        self.devices = []
    
    def add_device(self, device):
        self.devices.append(device)
    
    def remove_device(self, device_name):
        self.devices = [d for d in self.devices if d.name != device_name]
    
    def toggle_device(self, device_name):
        for device in self.devices:
            if device.name == device_name:
                device.toggle()
                return device
        return None

# GUI Application
class SmartHomeApp:
    def __init__(self, root):
        self.home = SmartHome()
        self.root = root
        self.root.title("Smart Home System")
        
        self.device_listbox = tk.Listbox(root, width=50)
        self.device_listbox.pack()
        
        self.add_button = tk.Button(root, text="Add Device", command=self.add_device)
        self.add_button.pack()
        
        self.toggle_button = tk.Button(root, text="Toggle Device", command=self.toggle_device)
        self.toggle_button.pack()
        
        self.remove_button = tk.Button(root, text="Remove Device", command=self.remove_device)
        self.remove_button.pack()
        
    def update_list(self):
        self.device_listbox.delete(0, tk.END)
        for device in self.home.devices:
            self.device_listbox.insert(tk.END, str(device))
    
    def add_device(self):
        name = "SmartLight" + str(len(self.home.devices) + 1)
        new_device = SmartLight(name)
        self.home.add_device(new_device)
        self.update_list()
    
    def toggle_device(self):
        selected = self.device_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a device to toggle")
            return
        
        device_name = self.device_listbox.get(selected[0]).split(" - ")[0]
        self.home.toggle_device(device_name)
        self.update_list()
    
    def remove_device(self):
        selected = self.device_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a device to remove")
            return
        
        device_name = self.device_listbox.get(selected[0]).split(" - ")[0]
        self.home.remove_device(device_name)
        self.update_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
