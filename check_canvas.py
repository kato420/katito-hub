import os
import json
from canvasapi import Canvas

API_URL = "https://utec.instructure.com"
API_KEY = os.getenv("CANVAS_API_KEY")  # Esto lo leerá de los Secrets de GitHub

canvas = Canvas(API_URL, API_KEY)
user = canvas.get_current_user()


def check():
    with open("data.json", "r") as f:
        data = json.load(f)

    # Mapa para coincidir nombres del JSON con Canvas
    mapping = {
        "Programacion III": "Programación III",
        "Base de Datos I": "Base de Datos I",
        "DBP": "Desarrollo Basado en Plataformas",
        "Metodos Numericos": "Métodos Numéricos",
    }

    all_courses = user.get_courses(enrollment_state="active")

    for c_key, c_canvas_name in mapping.items():
        course = next(
            (c for c in all_courses if hasattr(c, "name") and c_canvas_name in c.name),
            None,
        )
        if course:
            modules = course.get_modules()
            count = sum(len(list(m.get_module_items())) for m in modules)

            # Si el número de archivos cambió, marcamos como NUEVO
            short_key = (
                "Progra_3"
                if "Progra" in c_key
                else ("BD" if "Base" in c_key else c_key)
            )
            if data["cursos_status"][short_key]["archivos"] != count:
                data["cursos_status"][short_key]["nuevo"] = True
                data["cursos_status"][short_key]["archivos"] = count

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    check()
