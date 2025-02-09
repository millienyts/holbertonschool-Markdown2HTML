#!/usr/bin/env python3
import sys
import os
import hashlib
import re

# Function to parse headings in markdown and convert to HTML <h1> to <h6>
def parse_headings(line):
    heading_level = line.count('#')
    if heading_level in range(1, 7):
        return f"<h{heading_level}>{line.strip('#').strip()}</h{heading_level}>"
    return line

# Function to parse unordered lists (-) and convert to <ul> and <li>
def parse_unordered_list(lines):
    result = "<ul>\n"
    for line in lines:
        if line.startswith('-'):
            result += f"<li>{line[2:].strip()}</li>\n"
    result += "</ul>\n"
    return result

# Function to parse ordered lists (*) and convert to <ol> and <li>
def parse_ordered_list(lines):
    result = "<ol>\n"
    for line in lines:
        if line.startswith('*'):
            result += f"<li>{line[2:].strip()}</li>\n"
    result += "</ol>\n"
    return result

# Function to parse paragraph text and wrap in <p> tags
def parse_paragraph(lines):
    result = ""
    for line in lines:
        if line.strip():
            result += f"<p>{line.strip()}</p>\n"
    return result

# Function to parse bold and emphasis text in markdown
def parse_bold_italic(line):
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Bold
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)  # Emphasis
    return line

# Function to parse special cases: [[text]] -> MD5 and ((text)) -> remove 'c'/'C'
def parse_special_cases(line):
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)  # MD5
    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)  # Remove 'c' and 'C'
    return line

# Function to convert markdown content to HTML and write to file
def markdown_to_html(filename, output_file):
    with open(filename, 'r') as file:
        lines = file.readlines()

    html_content = ""
    for line in lines:
        line = parse_headings(line)
        line = parse_bold_italic(line)
        line = parse_special_cases(line)
        # Handle lists separately
        if line.startswith('-'):
            html_content += parse_unordered_list([line])
        elif line.startswith('*'):
            html_content += parse_ordered_list([line])
        else:
            html_content += parse_paragraph([line])

    with open(output_file, 'w') as file:
        file.write(html_content)

# Main function to handle arguments and control the script flow
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

