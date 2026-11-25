# ==========================================
# CONSTANTES DE CONFIGURACIÓN
# ==========================================
MIN_LONGITUD_NOMBRE = 2
MIN_DURACION_MINUTOS = 2
MIN_DESCARGAS = 1
UMBRAL_POPULARIDAD = 500


# ==========================================
# FUNCIONES DE VALIDACIÓN
# ==========================================

def validar_nombre(nombre: str) -> bool:
    """Retorna True si el nombre no es vacío/espacios y tiene al menos 2 caracteres."""
    return len(nombre.strip()) >= MIN_LONGITUD_NOMBRE


def validar_minutos(minutos: int) -> bool:
    """Retorna True si los minutos son mayores o iguales a 2."""
    return minutos >= MIN_DURACION_MINUTOS


def validar_descargas(descargas: int) -> bool:
    """Retorna True si las descargas son mayores que 0."""
    return descargas >= MIN_DESCARGAS


# ==========================================
# FUNCIONES DE ENTRADA Y MENÚ
# ==========================================

def mostrar_menu() -> None:
    """Muestra las opciones del menú principal en pantalla."""
    print(
        "\n========== MENÚ PRINCIPAL ==========\n"
        "1. Mostrar canciones\n"
        "2. Actualizar populares\n"
        "3. Eliminar canción\n"
        "4. Buscar canción\n"
        "5. Agregar canción\n"
        "6. Salir\n"
        "====================================="
    )


def leer_entero(mensaje: str) -> int | None:
    """Helper interno para capturar enteros de forma segura con try-except."""
    try:
        return int(input(mensaje))
    except ValueError:
        return None


def leer_opcion() -> int:
    """Lee, valida y retorna la opción numérica elegida por el usuario."""
    while True:
        opcion = leer_entero("Seleccione una opción (1-6): ")
        if opcion is not None and 1 <= opcion <= 6:
            return opcion
        print("Error: Debe ingresar un número entero válido entre 1 y 6.")


# ==========================================
# FUNCIONES DE GESTIÓN DE LA PLAYLIST
# ==========================================

def actualizar_populares(playlist: list[dict]) -> None:
    """Actualiza el campo 'popular' según si las descargas superan las 500."""
    for cancion in playlist:
        cancion["popular"] = cancion["descargas"] > UMBRAL_POPULARIDAD


def imprimir_detalle_cancion(cancion: dict) -> None:
    """Formatea e imprime los campos de una canción individual."""
    estado = "POPULAR" if cancion["popular"] else "ESTÁNDAR"
    print(
        f"Nombre: {cancion['nombre']}\n"
        f"Duración (min): {cancion['minutos']}\n"
        f"Descargas: {cancion['descargas']}\n"
        f"Estado: {estado}"
    )


def mostrar_canciones(playlist: list[dict]) -> None:
    """Actualiza estados y muestra todas las canciones de la lista."""
    actualizar_populares(playlist)

    if not playlist:
        print("\nLa playlist está vacía.")
        return

    print("\n=== LISTA DE CANCIONES ===")
    for cancion in playlist:
        imprimir_detalle_cancion(cancion)
        print("--------------------------------------------")


def buscar_cancion(playlist: list[dict], nombre_buscar: str) -> int:
    """Retorna el índice exacto (case-sensitive) de la canción, o -1 si no existe."""
    for indice, cancion in enumerate(playlist):
        if cancion["nombre"] == nombre_buscar:
            return indice
    return -1


def agregar_cancion(playlist: list[dict]) -> None:
    """Solicita datos, valida cada campo mediante funciones separadas y registra."""
    print("\n--- AGREGAR NUEVA CANCIÓN ---")

    nombre = input("Ingrese el nombre de la canción: ")
    if not validar_nombre(nombre):
        print("Error: El nombre no puede estar vacío ni tener menos de 2 caracteres. Canción no registrada.")
        return

    minutos = leer_entero("Ingrese la duración en minutos: ")
    if minutos is None or not validar_minutos(minutos):
        print("Error: La duración debe ser un número entero mayor o igual a 2. Canción no registrada.")
        return

    descargas = leer_entero("Ingrese el número de descargas: ")
    if descargas is None or not validar_descargas(descargas):
        print("Error: Las descargas deben ser un número entero mayor que 0. Canción no registrada.")
        return

    playlist.append({
        "nombre": nombre.strip(),
        "minutos": minutos,
        "descargas": descargas,
        "popular": False
    })
    print(f"Canción '{nombre.strip()}' agregada exitosamente.")


def eliminar_cancion(playlist: list[dict]) -> None:
    """Solicita el nombre, busca la canción y la elimina si existe."""
    nombre_eliminar = input("\nIngrese el nombre de la canción a eliminar: ")
    indice = buscar_cancion(playlist, nombre_eliminar)

    if indice != -1:
        eliminada = playlist.pop(indice)
        print(f"La canción '{eliminada['nombre']}' ha sido eliminada de la playlist.")
    else:
        print(f"La canción '{nombre_eliminar}' no se encuentra en la playlist.")


def consultar_cancion(playlist: list[dict]) -> None:
    """Solicita el nombre, busca la canción y muestra su posición (base 1) y datos."""
    nombre_buscar = input("\nIngrese el nombre de la canción a buscar: ")
    indice = buscar_cancion(playlist, nombre_buscar)

    if indice != -1:
        print(f"\nCanción encontrada en la posición {indice + 1}:")
        imprimir_detalle_cancion(playlist[indice])
    else:
        print(f"La canción '{nombre_buscar}' no se encuentra en la playlist.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main() -> None:
    playlist: list[dict] = []

    acciones = {
        1: mostrar_canciones,
        2: lambda pl: (actualizar_populares(pl), print("\nEstados de popularidad actualizados correctamente.")),
        3: eliminar_cancion,
        4: consultar_cancion,
        5: agregar_cancion,
    }

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 6:
            print("\nGracias por usar el gestor de playlist. ¡Hasta luego!")
            break

        acciones[opcion](playlist)


if __name__ == "__main__":
    main()