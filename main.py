import flet as ft
import yt_dlp
import os
import threading

def main(page: ft.Page):
    page.title = "Mi Música APK"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    titulo = ft.Text("Descargador de Música", size=26, weight=ft.FontWeight.BOLD)
    entrada = ft.TextField(label="Enlace o nombre de la canción", width=350, border_radius=10)
    estado = ft.Text("", size=14, text_align=ft.TextAlign.CENTER)
    progreso = ft.ProgressRing(visible=False)

    def proceso_descarga(query):
        try:
            ph.request_permission(ft.PermissionType.STORAGE)
            ruta = "/storage/emulated/0/Music"
            if not os.path.exists(ruta):
                ruta = os.path.expanduser("~")

            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': f'{ruta}/%(title)s.%(ext)s',
                'quiet': True,
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                busqueda = query if query.startswith("http") else f"ytsearch1:{query}"
                ydl.download([busqueda])

            estado.value = "¡Listo! Guardado en tu carpeta Música."
            estado.color = ft.Colors.GREEN_400
        except Exception as e:
            estado.value = f"Error: {str(e)}"
            estado.color = ft.Colors.RED_400
        finally:
            progreso.visible = False
            boton.disabled = False
            page.update()

    def al_presionar(e):
        if not entrada.value.strip():
            return
        boton.disabled = True
        progreso.visible = True
        estado.value = "Buscando y descargando audio..."
        estado.color = ft.Colors.WHITE
        page.update()
        threading.Thread(target=proceso_descarga, args=(entrada.value.strip(),), daemon=True).start()

    boton = ft.ElevatedButton(
        "Descargar Audio",
        icon=ft.Icons.DOWNLOAD,
        on_click=al_presionar,
        width=350,
        height=50,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
    )

    page.add(titulo, entrada, boton, progreso, estado)

ft.app(target=main)
