# importando librerias
import re
import os
import json
import string

try:
    # abriendo y leyendo archivo en caso de que ya exista
    with open("base_de_datos.json", "r") as archivo_db:
        print("Leyendo base de datos...")
        # cargando registros a lista de estudiantes
        lista_estudiantes = json.load(archivo_db)
        print("Base de datos cargada exitosamente!\n")
except:
    # en caso de que el archivo aun no exista
    print("Creando base de datos...\n")
    # lista estudiantes se inicializa vacia
    lista_estudiantes = []


def borrar_pantalla():
    # dependiendo del sistema operativo se usa el comando clear o cls
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")


def validar_nombre():
    while True:
        nombre_completo = input("\nIngrese nombre completo: ")
        # validando entrada del usuario con expresiones regulares (No Numeros, Minimo 2 Caracteres)
        if re.match('[a-zA-Z|ñÑ ]{1}[a-zA-Z?\s|ñÑ ]+$', nombre_completo):
            break
        else:
            print("Formato invalido, intentelo de nuevo!")

    # retornar el nombre completo
    return nombre_completo


def validar_carnet():
    while True:
        carnet = input("\nIngrese carnet: ")
        # validando entrada del usuario con expresiones regulares (YY-CCCC)
        if re.match('[0-9]{2}-[0-9]{4}$', carnet):
            break
        else:
            print("Formato invalido, intentelo de nuevo!")

    # retornar el carnet
    return carnet


def validar_nota():
    while True:
        nota = input("\nIngrese nota: ")
        # validando entrada del usuario con expresiones regulares (Solo Numeros, Entre 1 a 3 digitos)
        if re.match('[0-9]{1,3}$', nota):
            if int(nota) >= 0 and int(nota) <= 100:
                break
            else:
                print("Nota fuera de rango, intentelo de nuevo!")
        else:
            print("Formato invalido, intentelo de nuevo!")

    # retornar el nota
    return nota


def ingreso_notas():
    lista_notas = []
    opcion_notas = input("\nDesea ingresar una nota? (y / n): ")
    while opcion_notas == 'y' or opcion_notas == 'Y':
        nueva_nota = validar_nota()
        # convertir en entero
        nueva_nota = int(nueva_nota)
        lista_notas.append(nueva_nota)
        opcion_notas = input("\nDesea ingresar otra nota? (y / n): ")

    return lista_notas


def calcular_promedio(lista_notas_estudiante):
    # calcular promedio
    promedio = sum(lista_notas_estudiante) / len(lista_notas_estudiante)

    # retornar el promedio
    return promedio


def calcular_porcentaje(cantidad_cursos_aprobados, cantidad_cursos_asignados):
    # calcular porcentaje
    porcentaje = (cantidad_cursos_aprobados / cantidad_cursos_asignados) * 100

    # retornar el porcentaje
    return porcentaje


def ingresar_nuevo_estudiante():
    # pedir datos de estudiante
    nombre = validar_nombre()
    while True:
        carnet = validar_carnet()
        consulta = buscar_estudiante(carnet)
        if consulta:
            print("Este carnet ya ha sido registrado, intentelo de nuevo!")
        else:
            break
    # agregar notas

    while True:
        lista_notas = ingreso_notas()
        if len(lista_notas) == 0:
            print('\nNo se puede ingresar un estudiante sin notas!')
        else:
            break

    # calculado año de ingreso segun el carnet
    anno_de_ingreso = "20" + carnet.split('-')[0]
    # agregar cursos aprobados
    cursos_aprobados = [note for note in lista_notas if note >= 61]
    # llamar al calculo de promedio
    promedio_estudiante = calcular_promedio(lista_notas)
    # llamar al calculo de porcentaje
    porcentaje_cursos_aprobados = calcular_porcentaje(
        len(cursos_aprobados), len(lista_notas))
    # crear al nuevo estudiante
    estudiante = {
        'nombre_completo': nombre,
        'carnet': carnet,
        'notas': lista_notas,
        'anno_ingreso': anno_de_ingreso,
        'cursos_asignados': len(lista_notas),
        'promedio_notas': promedio_estudiante,
        'cursos_aprobados': len(cursos_aprobados),
        'porcentaje_cursos_aprobados': porcentaje_cursos_aprobados,
    }

    # agregar el nuevo estudiante a la lista
    lista_estudiantes.append(estudiante)

    return


def imprimir_estudiante(estudiante):
    # imprimiendo las propiedades del estudiante
    print(f"Nombre: {estudiante['nombre_completo']}")
    print(f"Carnet: {estudiante['carnet']}")
    print(f"Notas: {estudiante['notas']}")
    print(f"Año de ingreso: {estudiante['anno_ingreso']}")
    print(f"Cursos asignados: {estudiante['cursos_asignados']}")
    print("Promedio de notas: {0:.2f}".format(estudiante['promedio_notas']))
    print(f"Cursos aprobados: {estudiante['cursos_aprobados']}")
    print("Porcentaje de cursos aprobados: {0:.2f} %".format(
        estudiante['porcentaje_cursos_aprobados']))
    print('--------------------------------------------------')

    return


def buscar_estudiante(carnet):
    # buscando estudiante por carnet de lista estudiantes
    consulta = next(
        (estudiante for estudiante in lista_estudiantes if estudiante['carnet'] == carnet), 0)

    if consulta:
        return consulta
    else:
        return 0


def mostrar_lista_estudiantes():
    # iterando por estudiante de lista estudiantes
    print('\nListado de estudiantes\n')
    print('--------------------------------------------------')
    for estudiante in lista_estudiantes:
        # llamando a funcion imprimir_estudiante
        imprimir_estudiante(estudiante)

    cantidad_estudiantes = len(lista_estudiantes)
    print(f'\nTotal de estudiantes registrados: {cantidad_estudiantes}')

    return


def mostrar_menu():
    mensaje_menu = """
Registro de estudiantes

1. Ingresar un nuevo estudiante
2. Buscar un estudiante por carnet
3. Mostrar el listado de estudiantes
4. Salir

Ingrese la opcion deseada: """

    # mostrar menu de navegacion
    opcion = input(mensaje_menu)
    borrar_pantalla()
    if opcion == '1':
        # ingresar un nuevo estudiante
        ingresar_nuevo_estudiante()

    if opcion == '2':
        # buscar un estudiante por carnet
        carnet = validar_carnet()
        print('\nBuscando estudiante...')
        estudiante = buscar_estudiante(carnet)
        if estudiante:
            print('\nEstudiante encontrado!\n')
            print('--------------------------------------------------')
            imprimir_estudiante(estudiante)
        else:
            print('\nEstudiante no encontrado!')

    if opcion == '3':
        # mostrar cantidad y el listado de estudiantes
        mostrar_lista_estudiantes()

    if opcion == '4':
        mostrar_submenu_salir()
        return

    mostrar_menu()
    return


def mostrar_submenu_salir():
    mensaje_submenu = """
Submenu

1. Guardar y salir
2. Salir sin guardar

Ingrese la opcion deseada: """

    # mostrar submenu de salir
    opcion_submenu = input(mensaje_submenu)
    borrar_pantalla()
    if opcion_submenu == '1':
        # guardando lista_estudiantes en archivo base_de_datos.json
        with open("base_de_datos.json", "w") as archivo_db:
            print("Guardando base de datos...")
            json.dump(lista_estudiantes, archivo_db)

        return

    if opcion_submenu == '2':
        # salir sin guardar
        return

    mostrar_submenu_salir()
    return


mostrar_menu()
