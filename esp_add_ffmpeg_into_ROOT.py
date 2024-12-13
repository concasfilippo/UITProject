import winreg as reg
import os

#da ricontrollare perché non aggiungere ffmpeg\bin

def add_ffmpeg_to_path(ffmpeg_path):
    try:
        # Apri la chiave di registro per le variabili d'ambiente di sistema
        reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                              0, reg.KEY_READ | reg.KEY_WRITE)

        # Leggi il valore corrente del PATH
        current_path, _ = reg.QueryValueEx(reg_key, "Path")

        # Aggiungi il percorso di FFmpeg se non è già presente
        if ffmpeg_path not in current_path:
            new_path = current_path + os.pathsep + ffmpeg_path
            print(new_path)
            reg.SetValueEx(reg_key, "Path", 0, reg.REG_EXPAND_SZ, new_path)
            print("FFmpeg aggiunto al PATH con successo.")
        else:
            print("FFmpeg è già nel PATH.")

        reg.CloseKey(reg_key)
    except PermissionError:
        print("Devi eseguire questo script come amministratore per modificare il registro.")
    except Exception as e:
        print(f"Errore: {e}")


# Specifica il percorso della cartella "bin" di FFmpeg
ffmpeg_path = r"ffmpeg\bin"
add_ffmpeg_to_path(ffmpeg_path)