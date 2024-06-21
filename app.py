import os
import json
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from datetime import datetime
import hashlib
import base64
import shutil

def get_chrome_profiles():
    # Caminho para a pasta do Chrome
    chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
    local_state_path = os.path.join(chrome_path, 'Local State')

    # Fazendo backup do arquivo Local State
    backup_path = f"{local_state_path}.BAK-{datetime.now().strftime('%Y%m%d')}"
    shutil.copy(local_state_path, backup_path)

    # Lendo o arquivo 'Local State'
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)

    # Extraindo perfis
    profiles = local_state['profile']['info_cache']
    return profiles, chrome_path, local_state_path

password_file = "profile_lock.json"

def load_passwords():
    if os.path.exists(password_file):
        with open(password_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_passwords(passwords):
    with open(password_file, 'w', encoding='utf-8') as file:
        json.dump(passwords, file)

def encrypt_password(password):
    return base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()

class ChromeProfileLocker:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrome Profile Locker")
        self.root.iconbitmap('app_icon.ico')
        self.root.geometry('750x570')
        self.root.minsize(670, 530)
        self.root.configure(bg='#f9f9f9')

        self.profiles, self.chrome_path, self.local_state_path = get_chrome_profiles()
        self.passwords = load_passwords()

        self.create_menu()
        self.create_header()
        self.create_widgets()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)

    def show_about(self):
        messagebox.showinfo("Sobre", "Chrome Profile Locker\nVersão 1.0\nGerencie e proteja seus perfis do Chrome com facilidade.")

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#f9f9f9')
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Chrome Profile Locker", font=("Helvetica", 16, "bold"), bg='#f9f9f9')
        title_label.pack(side="left", padx=10)

        subtitle_label = tk.Label(header_frame, text="Gerencie e proteja seus perfis do Chrome", font=("Helvetica", 12), bg='#f9f9f9')
        subtitle_label.pack(side="left", padx=10)

        logo_image = Image.open('app_logo.png')
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(header_frame, image=logo_photo, bg='#f9f9f9')
        logo_label.image = logo_photo
        logo_label.pack(side="right", padx=10)

    def create_widgets(self):
        profiles_frame = tk.Frame(self.root, bg='#f9f9f9')
        profiles_frame.pack(padx=10, pady=10)

        # Verificar e criar a pasta Avatars se não existir
        avatars_path = os.path.join(self.chrome_path, 'Avatars')
        if not os.path.exists(avatars_path):
            os.makedirs(avatars_path)
            shutil.copy('avatar_soccer.png', avatars_path)

        row, col = 0, 0
        for profile, info in self.profiles.items():
            frame = tk.Frame(profiles_frame, relief=tk.RAISED, borderwidth=1, bg='#f9f9f9')
            frame.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10)

            image_path = os.path.join(self.chrome_path, profile, "Google Profile Picture.png")
            if not os.path.exists(image_path):
                image_path = "default_profile.png"

            profile_image = Image.open(image_path)
            profile_image = profile_image.resize((100, 100), Image.LANCZOS)
            profile_photo = ImageTk.PhotoImage(profile_image)

            profile_image_label = tk.Label(frame, image=profile_photo, bg='#f9f9f9')
            profile_image_label.image = profile_photo  # Referência para manter a imagem na memória
            profile_image_label.pack()

            profile_label = tk.Label(frame, text=info['name'], bg='#f9f9f9')
            profile_label.pack(pady=(5, 10))

            button_text = "Desbloquear" if profile in self.passwords else "Bloquear"
            action_button = tk.Button(frame, text=button_text, command=lambda p=profile: self.toggle_lock_profile(p))
            action_button.pack(pady=5)

            col += 1
            if col == 4:  # Número de perfis por linha
                col = 0
                row += 1

    def toggle_lock_profile(self, profile):
        if profile in self.passwords:
            self.unlock_profile(profile)
        else:
            self.lock_profile(profile)

    def lock_profile(self, profile):
        password = simpledialog.askstring("Senha", "Digite a senha para bloquear o perfil:", show='*')
        if password:
            encrypted_password = encrypt_password(password)
            self.passwords[profile] = encrypted_password
            save_passwords(self.passwords)
            self.update_local_state(profile, lock=True)
            self.update_widgets()
            messagebox.showinfo("Info", f"Perfil {self.profiles[profile]['name']} bloqueado.")

    def unlock_profile(self, profile):
        password = simpledialog.askstring("Senha", "Digite a senha para desbloquear o perfil:", show='*')
        encrypted_password = encrypt_password(password)
        if encrypted_password == self.passwords.get(profile):
            del self.passwords[profile]
            save_passwords(self.passwords)
            self.update_local_state(profile, lock=False)
            self.update_widgets()
            messagebox.showinfo("Info", f"Perfil {self.profiles[profile]['name']} desbloqueado.")
        else:
            messagebox.showerror("Erro", "Senha incorreta.")

    def update_local_state(self, profile, lock):
        with open(self.local_state_path, 'r+', encoding='utf-8') as file:
            local_state = json.load(file)
            if lock:
                local_state['profile']['info_cache'][profile]['avatar_icon'] = "chrome://theme/IDR_PROFILE_AVATAR_17"
                os.rename(os.path.join(self.chrome_path, profile), os.path.join(self.chrome_path, f"{profile} - LOCK"))
            else:
                local_state['profile']['info_cache'][profile]['avatar_icon'] = "chrome://theme/IDR_PROFILE_AVATAR_26"
                os.rename(os.path.join(self.chrome_path, f"{profile} - LOCK"), os.path.join(self.chrome_path, profile))

            file.seek(0)
            json.dump(local_state, file)
            file.truncate()

    def update_widgets(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget is not self.root.winfo_children()[0]:  # Ignorar o frame do cabeçalho
                widget.destroy()
        self.create_widgets()

# Criando a aplicação
root = tk.Tk()
app = ChromeProfileLocker(root)
root.mainloop()
