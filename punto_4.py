# =====================================================================
# PUNTO 4: IMPLEMENTACIÓN DE LOS AUTÓMATAS FINITOS DETERMINÍSTICOS (AFD)
# =====================================================================

# Conjunto de Palabras Reservadas para la discriminación posterior
KEYWORDS = {
    "int", "float", "bool", "void", "if", "else", "while", 
    "for", "return", "print", "read", "true", "false"
}

def auto_id_o_keyword(texto, inicio):
    """
    AFD para Identificadores y Palabras Reservadas.
    S0: inicial, S1: aceptación.
    """
    estado = 0
    cursor = inicio
    lexema = ""
    
    while cursor < len(texto):
        caracter = texto[cursor]
        
        if estado == 0:
            if caracter.isalpha() or caracter == '_':
                estado = 1
                lexema += caracter
            else:
                return None  # Error: no empieza con letra o guion bajo
                
        elif estado == 1:
            if caracter.isalnum() or caracter == '_':
                lexema += caracter
            else:
                # Transición a "Otro" -> Corta y acepta lo acumulado
                break
        cursor += 1
        
    if estado == 1:
        # Si el lexema acumulado es una palabra reservada, cambia el tipo de token
        tipo = lexema if lexema in KEYWORDS else "id"
        return (tipo, lexema, cursor)
    return None


def auto_num(texto, inicio):
    """
    AFD para Literales Numéricos (Enteros y Flotantes).
    S0: inicial, S1: entero, S2: punto leído, S3: flotante.
    """
    estado = 0
    cursor = inicio
    lexema = ""
    
    while cursor < len(texto):
        caracter = texto[cursor]
        
        if estado == 0:
            if caracter.isdigit():
                estado = 1
                lexema += caracter
            else:
                return None
                
        elif estado == 1:
            if caracter.isdigit():
                lexema += caracter
            elif caracter == '.':
                estado = 2
                lexema += caracter
            else:
                break  # Acepta entero
                
        elif estado == 2:
            if caracter.isdigit():
                estado = 3
                lexema += caracter
            else:
                return None  # Error: Estructura inválida (ej: '12.')
                
        elif estado == 3:
            if caracter.isdigit():
                lexema += caracter
            else:
                break  # Acepta flotante
        cursor += 1
        
    if estado in (1, 3):
        return ("num", lexema, cursor)
    return None


def auto_str(texto, inicio):
    """
    AFD para Literales de Cadena (Strings).
    S0: inicial, S1: leyendo caracteres, S2: comilla de cierre (aceptación).
    """
    estado = 0
    cursor = inicio
    lexema = ""
    
    while cursor < len(texto):
        caracter = texto[cursor]
        
        if estado == 0:
            if caracter == '"':
                estado = 1
                lexema += caracter
            else:
                return None
                
        elif estado == 1:
            lexema += caracter
            if caracter == '"':
                estado = 2
                cursor += 1
                break
            elif caracter == '\n':
                return None  # Error: Salto de línea sin cerrar la cadena
                
        cursor += 1
        
    if estado == 2:
        return ("str", lexema, cursor)
    return None

def auto_asignacion_o_igualdad(texto, inicio):
    """
    AFD para '=' y '=='.
    """
    if inicio >= len(texto) or texto[inicio] != '=':
        return None
        
    # Miramos el siguiente caracter (Lookahead)
    if inicio + 1 < len(texto) and texto[inicio + 1] == '=':
        return ("==", "==", inicio + 2)
    return ("=", "=", inicio + 1)

def auto_relacionales_y_not(texto, inicio):
    """
    AFD para operadores que pueden llevar un '=' opcional: <, <=, >, >=, !, !=
    """
    if inicio >= len(texto):
        return None
        
    caracter = texto[inicio]
    if caracter not in ('<', '>', '!'):
        return None
        
    # Verificamos si el siguiente es un '='
    if inicio + 1 < len(texto) and texto[inicio + 1] == '=':
        op_compuesto = caracter + '='
        return (op_compuesto, op_compuesto, inicio + 2)
    return (caracter, caracter, inicio + 1)

def auto_logicos_dobles(texto, inicio):
    """
    AFD para '&&' y '||'. 
    Exige la duplicación exacta del símbolo.
    """
    if inicio + 1 >= len(texto):
        return None
        
    caracteres = texto[inicio:inicio+2]
    if caracteres in ("&&", "||"):
        return (caracteres, caracteres, inicio + 2)
    return None

def auto_delimitadores_y_aritmeticos(texto, inicio):
    """
    AFD para tokens rígidos de un solo carácter: +, -, *, /, (, ), {, }, ;, ,
    """
    if inicio >= len(texto):
        return None
        
    caracter = texto[inicio]
    simbolos_simples = {'+', '-', '*', '/', '(', ')', '{', '}', ';', ','}
    
    if caracter in simbolos_simples:
        return (caracter, caracter, inicio + 1)
    return None
