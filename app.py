from tkinter import *
from tkinter import ttk, filedialog
from pytube import YouTube
import os

def download_audio():
    url = url_entry.get()
    if url == placeholder_text:
        status_label.config(text="Por favor, insira uma URL válida.", foreground="#ff0000")  # Cor vermelha
        return

    try:
        # Verifica se a URL é válida
        yt = YouTube(url)

        # Obtendo as streams de áudio
        audio_streams = yt.streams.filter(only_audio=True)
        if not audio_streams:
            status_label.config(text="Nenhum áudio encontrado para este link.", foreground="#ff00ff")
            return

        # Selecionando a melhor stream de áudio disponível (maior taxa de bits)
        audio_stream = audio_streams.order_by('abr').desc().first()

        # Abrir a caixa de diálogo para selecionar o diretório de destino
        destination_folder = filedialog.askdirectory()
        if not destination_folder:
            status_label.config(text="Download cancelado pelo usuário.", foreground="#ff00ff")
            return

        # Fazer o download do áudio
        out_file = audio_stream.download(output_path=destination_folder)

        # Convertendo para MP3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        status_label.config(text="Download concluído com sucesso!", foreground="#00ff00")  # Cor verde
        save_path_label.config(text=f"Arquivo salvo em: {new_file}", foreground="#00ff00")

    except Exception as e:
        status_label.config(text=f"Ocorreu um erro: {str(e)}", foreground="#ff00ff")  # Mostra a mensagem de erro

def on_entry_click(event):
    """Remove o placeholder do campo de entrada quando o usuário clica no campo"""
    if url_entry.get() == placeholder_text:
        url_entry.delete(0, "end")  # Limpa o conteúdo do campo de entrada
        url_entry.config(foreground="black")

def on_focusout(event):
    """Adiciona o placeholder se o campo de entrada estiver vazio quando o usuário sair do campo"""
    if url_entry.get() == "":
        url_entry.insert(0, placeholder_text)
        url_entry.config(foreground="grey")

# tkinter
janela = Tk()
janela.title("Conversor de vídeos do YouTube")
janela.geometry("775x275")
janela.configure(bg="#99b3b1")  # background azul esverdiado

style = ttk.Style(janela)
style.theme_use('clam')

# Estilos
style.configure('TButton', background="#0378a6", foreground='white', font=('Arial', 10), padding=5)
style.map('TButton', background=[('active', '#5E2E7A')])  # Mudança de cor ao clicar
style.configure('TLabel', background="#99b3b1", foreground='#34495E', font=('Arial', 14))

# Placeholder
placeholder_text = "Digite ou dê ctrl + v aqui:"

# Layout
texto_orientacao = ttk.Label(janela, text="Converta e baixe vídeos do YouTube em áudio", style='TLabel')
texto_orientacao.grid(column=0, row=0, pady=(20, 5), padx=175)

url_entry = ttk.Entry(janela, width=78, foreground="grey")
url_entry.grid(column=0, row=1, padx=10)
url_entry.insert(0, placeholder_text)
url_entry.bind('<FocusIn>', on_entry_click)
url_entry.bind('<FocusOut>', on_focusout)

# Botão de download
botao = ttk.Button(janela, text="Baixar", command=download_audio, style='TButton')
botao.grid(column=0, row=2, pady=(10, 5), padx=10)

# Labels de status
status_label = ttk.Label(janela, text="", font=('Arial', 12, 'italic'), background="#99b3b1")
status_label.grid(column=0, row=3, pady=(5, 5), padx=10)

save_path_label = ttk.Label(janela, text="", font=('Arial', 12), background="#99b3b1")
save_path_label.grid(column=0, row=4, pady=(0, 10), padx=10)

janela.mainloop()