import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

def get_chrome_profiles():
    # Caminho para a pasta do Chrome
    chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
    local_state_path = os.path.join(chrome_path, 'Local State')

    # Lendo o arquivo 'Local State'
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)

    # Extraindo perfis
    profiles = local_state['profile']['info_cache']
    return profiles, chrome_path

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

        self.profiles, self.chrome_path = get_chrome_profiles()
        self.passwords = load_passwords()
        self.create_widgets()

    def create_widgets(self):
        row, col = 0, 0
        for profile, info in self.profiles.items():
            frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10)

            image_path = os.path.join(self.chrome_path, profile, "Google Profile Picture.png")
            if not os.path.exists(image_path):
                image_path = "default_profile.png"

            profile_image = Image.open(image_path)
            profile_image = profile_image.resize((100, 100), Image.ANTIALIAS)
            profile_photo = ImageTk.PhotoImage(profile_image)

            profile_image_label = tk.Label(frame, image=profile_photo)
            profile_image_label.image = profile_photo # mantendo uma referência para evitar o garbage collector
            profile_image_label.pack()

            profile_label = tk.Label(frame, text=info['name'])
            profile_label.pack(pady=(5, 10))

            lock_button = tk.Button(frame, text="Bloquear", command=lambda p=profile: self.lock_profile(p))
            lock_button.pack(side="left", padx=5, pady=5)

            unlock_button = tk.Button(frame, text="Desbloquear", command=lambda p=profile: self.unlock_profile(p))
            unlock_button.pack(side="right", padx=5, pady=5)

            col += 1
            if col == 4: # 4 perfis por linha
                col = 0
                row += 1

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
