# =====================================================================
# PUNTO 5: IMPLEMENTACIÓN DEL PROGRAMA PRINCIPAL (MÓDULO CENTRAL)
# Fase de Coordinación Secuencial y Control del Lexer
# =====================================================================

def lexer(codigo_fuente):
    """
    Analizador Lexicográfico principal para el lenguaje Mini-C.
    Recibe una cadena de caracteres y devuelve una lista de pares (tipo_token, lexema).
    """
    tokens_validos = []
    cursor = 0
    longitud = len(codigo_fuente)
    
    # Lista ordenada de autómatas para asegurar la prioridad léxica correcta.
    # Evita ambigüedades procesando operadores compuestos antes que los simples.
    automatas = [
        auto_id_o_keyword,
        auto_num,
        auto_str,
        auto_asignacion_o_igualdad,
        auto_relacionales_y_not,
        auto_logicos_dobles,
        auto_delimitadores_y_aritmeticos
    ]
    
    while cursor < longitud:
        caracter_actual = codigo_fuente[cursor]
        
        # 1. Ignorar caracteres de descarte (espacios, tabulaciones, saltos de línea)
        if caracter_actual in (' ', '\t', '\n'):
            cursor += 1
            continue
            
        # Variable testigo para verificar si algún autómata tuvo éxito
        token_reconocido = False
        
        # 2. Evaluación secuencial de la batería de autómatas
        for automata in automatas:
            resultado = automata(codigo_fuente, cursor)
            
            if resultado is not None:
                tipo_token, lexema, nueva_posicion = resultado
                
                # Almacena el par estructurado exigido por la cátedra
                tokens_validos.append((tipo_token, lexema))
                
                # Desplaza el cursor al final del bloque procesado con éxito
                cursor = nueva_posicion
                token_reconocido = True
                break  # Rompe el lazo for para iniciar una nueva búsqueda desde el nuevo índice
                
        # 3. Manejo de Errores: Si ningún AFD reconoce la entrada actual
        if not token_reconocido:
            # Captura un entorno de 10 caracteres para contextualizar el fallo en la consola
            contexto_error = codigo_fuente[cursor:cursor+10].replace('\n', ' ')
            print(f">>> ERROR LEXICOGRÁFICO: Estructura incorrecta o carácter inválido en la posición {cursor}.")
            print(f"    Secuencia detectada: '{contexto_error}...'")
            return None  # Cancela el proceso devolviendo un estado nulo
            
    return tokens_validos
