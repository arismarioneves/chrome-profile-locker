import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

def get_chrome_profiles():
    # Caminho para a pasta do Chrome
    chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
    local_state_path = os.path.join(chrome_path, 'Local State')

    # Lendo o arquivo 'Local State'
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)

    # Extraindo perfis
    profiles = local_state['profile']['info_cache']
    return profiles

password_file = "profile_passwords.json"

def load_passwords():
    if os.path.exists(password_file):
        with open(password_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_passwords(passwords):
    with open(password_file, 'w', encoding='utf-8') as file:
        json.dump(passwords, file)

class ChromeProfileLocker:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrome Profile Locker")

        self.profiles = get_chrome_profiles()
        self.passwords = load_passwords()
        self.create_widgets()

    def create_widgets(self):
        for profile, info in self.profiles.items():
            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=5, pady=5)

            profile_label = tk.Label(frame, text=info['name'])
            profile_label.pack(side="left", padx=5, pady=5)

            lock_button = tk.Button(frame, text="Bloquear", command=lambda p=profile: self.lock_profile(p))
            lock_button.pack(side="right", padx=5, pady=5)

            unlock_button = tk.Button(frame, text="Desbloquear", command=lambda p=profile: self.unlock_profile(p))
            unlock_button.pack(side="right", padx=5, pady=5)

    def lock_profile(self, profile):
        password = tk.simpledialog.askstring("Senha", "Digite a senha para bloquear o perfil:", show='*')
        if password:
            self.passwords[profile] = password
            save_passwords(self.passwords)
            messagebox.showinfo("Info", f"Perfil {self.profiles[profile]['name']} bloqueado.")

    def unlock_profile(self, profile):
        password = tk.simpledialog.askstring("Senha", "Digite a senha para desbloquear o perfil:", show='*')
        if password == self.passwords.get(profile):
            messagebox.showinfo("Info", f"Perfil {self.profiles[profile]['name']} desbloqueado.")
        else:
            messagebox.showerror("Erro", "Senha incorreta.")

# Criando a aplicação
root = tk.Tk()
app = ChromeProfileLocker(root)
root.mainloop()
