import os
import json
from canvasapi import Canvas

API_URL = "https://utec.instructure.com"
API_KEY = os.getenv("CANVAS_API_KEY")


def check():
    try:
        canvas = Canvas(API_URL, API_KEY)
        user = canvas.get_current_user()

        with open("data.json", "r") as f:
            data = json.load(f)

        # Mapa exacto basado en tu consolidado
        mapping = {
            "Progra_3": "Programación III",
            "BD": "Base de Datos I",
            "DBP": "Desarrollo Basado en Plataformas",
            "Metodos": "Métodos Numéricos",
        }

        all_courses = list(user.get_courses(enrollment_state="active"))

        for json_key, canvas_name in mapping.items():
            course = next(
                (
                    c
                    for c in all_courses
                    if hasattr(c, "name") and canvas_name.lower() in c.name.lower()
                ),
                None,
            )

            if course:
                modules = course.get_modules()
                count = 0
                for m in modules:
                    count += len(list(m.get_module_items()))

                # Actualizar si hay cambios
                if data["cursos_status"][json_key]["archivos"] != count:
                    data["cursos_status"][json_key]["nuevo"] = True
                    data["cursos_status"][json_key]["archivos"] = count

        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Error detectado: {e}")
        exit(1)


if __name__ == "__main__":
    check()
