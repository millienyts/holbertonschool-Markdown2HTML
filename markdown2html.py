#!/usr/bin/python3
import sys
import os
import hashlib
import re

# Función para manejar los encabezados de markdown a HTML
def parse_headings(line):
    heading_level = line.count('#')
    if heading_level in range(1, 7):  # solo para encabezados válidos (# a ######)
        return f"<h{heading_level}>{line.strip('#').strip()}</h{heading_level}>"
    return line

# Función para manejar listas no ordenadas (con "-")
def parse_unordered_list(lines):
    result = "<ul>\n"
    for line in lines:
        if line.startswith('-'):
            result += f"<li>{line[2:].strip()}</li>\n"
    result += "</ul>\n"
    return result

# Función para manejar listas ordenadas (con "*")
def parse_ordered_list(lines):
    result = "<ol>\n"
    for line in lines:
        if line.startswith('*'):
            result += f"<li>{line[2:].strip()}</li>\n"
    result += "</ol>\n"
    return result

# Función para manejar párrafos
def parse_paragraph(lines):
    result = ""
    for line in lines:
        if line.strip():  # Solo agregar si no está vacío
            result += f"<p>{line.strip()}</p>\n"
    return result

# Función para manejar negrita y énfasis en el texto
def parse_bold_italic(line):
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Convertir **bold**
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)  # Convertir __emphasis__
    return line

# Función para manejar los casos especiales
def parse_special_cases(line):
    # Convertir [[texto]] a MD5
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
    # Eliminar todas las "c" y "C" de ((texto))
    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)
    return line

# Función principal para convertir el markdown a HTML
def markdown_to_html(filename, output_file):
    with open(filename, 'r') as file:
        lines = file.readlines()

    html_content = ""
    for line in lines:
        line = parse_headings(line)
        line = parse_bold_italic(line)
        line = parse_special_cases(line)
        
        # Procesar listas
        if line.startswith('-'):
            html_content += parse_unordered_list([line])
        elif line.startswith('*'):
            html_content += parse_ordered_list([line])
        else:
            html_content += parse_paragraph([line])

    with open(output_file, 'w') as file:
        file.write(html_content)

# Función para manejar los argumentos y errores
def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(markdown_file, html_file)
    sys.exit(0)

if __name__ == "__main__":
    main()
