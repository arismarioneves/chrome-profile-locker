# Chrome Profile Locker

> 🛑 **ATENÇÃO:** Aplicação em desenvolvimento. Este software ainda não foi testado em diferentes sistemas operacionais e versões do Google Chrome, podendo apresentar problemas de compatibilidade e causar perda de dados.

Chrome Profile Locker é um software que permite bloquear perfis do Google Chrome com senha. Este aplicativo lê os perfis do Chrome e exibe uma interface gráfica onde você pode bloquear e desbloquear perfis específicos.

![Chrome Profile Locker](https://github.com/arismarioneves/chrome-profile-locker/blob/main/screenshot.png)

## Sistema Operacional

- Windows (em desenvolvimento)
- Linux (não implementado)
- macOS (não implementado)

## Google Chrome
- Google Chrome (Versão 126.0.6478.114 (Versão oficial) 64 bits)

  > A aplicação foi testado apenas na versão acima.

## Pré-requisitos

- Python 3.x
- Pillow (biblioteca de manipulação de imagens)
- PyInstaller (para compilar o executável)

## Instalação

1. Clone este repositório:

    ```
    git clone https://github.com/arismarioneves/chrome-profile-locker.git
    cd chrome-profile-locker
    ```

2. Instale as dependências:

    ```
    pip install -r requirements.txt
    ```

3. Certifique-se de ter os seguintes arquivos na mesma pasta que o script principal:

    - `app_icon.ico` (ícone da aplicação)
    - `app_logo.png` (logo da aplicação)
    - `avatar_soccer.png` (imagem de avatar padrão)
    - `default_profile.png` (imagem de perfil padrão)

## Uso

1. Execute o script principal:

    ```
    python app.py
    ```

2. Uma interface gráfica será exibida com todos os perfis do Chrome. Você pode bloquear ou desbloquear um perfil clicando no botão correspondente.

## Compilação para Executável

Para compilar o script em um executável, use o PyInstaller:

1. Instale o PyInstaller:

    ```
    pip install pyinstaller
    ```

2. Compile o executável:

    ```
    pyinstaller --onefile --windowed --icon=app_icon.ico seu_arquivo.py
    ```

3. O executável será gerado na pasta `dist`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.
