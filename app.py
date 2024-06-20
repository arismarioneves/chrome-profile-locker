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
        self.root.iconbitmap('app_icon.ico')
        self.root.configure(bg='#f9f9f9')

        self.profiles, self.chrome_path = get_chrome_profiles()
        self.passwords = load_passwords()

        self.create_header()
        self.create_widgets()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#f9f9f9')
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Chrome Profile Locker", font=("Helvetica", 16, "bold"), bg='#f9f9f9')
        title_label.pack(side="left", padx=10)

        subtitle_label = tk.Label(header_frame, text="Gerencie e proteja seus perfis do Chrome", font=("Helvetica", 12), bg='#f9f9f9')
        subtitle_label.pack(side="left", padx=10)

        logo_image = Image.open('app_logo.png')
        logo_image = logo_image.resize((50, 50), Image.ANTIALIAS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(header_frame, image=logo_photo, bg='#f9f9f9')
        logo_label.image = logo_photo
        logo_label.pack(side="right", padx=10)

    def create_widgets(self):
        row, col = 0, 0
        for profile, info in self.profiles.items():
            frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1, bg='#f9f9f9')
            frame.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10)

            image_path = os.path.join(self.chrome_path, profile, "Google Profile Picture.png")
            if not os.path.exists(image_path):
                image_path = "default_profile.png"

            profile_image = Image.open(image_path)
            profile_image = profile_image.resize((100, 100), Image.ANTIALIAS)
            profile_photo = ImageTk.PhotoImage(profile_image)

            profile_image_label = tk.Label(frame, image=profile_photo, bg='#f9f9f9')
            profile_image_label.image = profile_photo # mantendo uma referência para evitar o garbage collector
            profile_image_label.pack()

            profile_label = tk.Label(frame, text=info['name'], bg='#f9f9f9')
            profile_label.pack(pady=(5, 10))

            button_text = "Desbloquear" if profile in self.passwords else "Bloquear"
            action_button = tk.Button(frame, text=button_text, command=lambda p=profile: self.toggle_lock_profile(p))
            action_button.pack(pady=5)

            col += 1
            if col == 4: # 4 perfis por linha
                col = 0
                row += 1

    def toggle_lock_profile(self, profile):
        if profile in self.passwords:
            self.unlock_profile(profile)
        else:
            self.lock_profile(profile)

    def lock_profile(self, profile):
        password = tk.simpledialog.askstring("Senha", "Digite a senha para bloquear o perfil:", show='*')
        if password:
            self.passwords[profile] = password
            save_passwords(self.passwords)
            self.update_widgets()
            messagebox.showinfo("Info", f"Perfil {self.profiles[profile]['name']} bloqueado.")

    def unlock_profile(self, profile):
        password = tk.simpledialog.askstring("Senha", "Digite a senha para desbloquear o perfil:", show='*')
        if password == self.passwords.get(profile):
            del self.passwords[profile]
            save_passwords(self.passwords)
            self.update_widgets()
            messagebox.showinfo("Info", f"Perfil {self.profiles[profile]['name']} desbloqueado.")
        else:
            messagebox.showerror("Erro", "Senha incorreta.")

    def update_widgets(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget is not self.root.winfo_children()[0]: # Ignorando o frame do título
                widget.destroy()
        self.create_widgets()

# Criando a aplicação
root = tk.Tk()
app = ChromeProfileLocker(root)
root.mainloop()
