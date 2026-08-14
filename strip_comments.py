import os
import tokenize
import io

def remove_comments(source_code):
    tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)
    out = ""
    last_lineno = -1
    last_col = 0
    for tok in tokens:
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        
        if token_type == tokenize.COMMENT:
            pass # skip comment
        else:
            out += token_string
            
        last_lineno = end_line
        last_col = end_col
        
    out_lines = []
    for line in out.split('\n'):
        if not line.strip() and (not out_lines or not out_lines[-1].strip()):
            continue
        out_lines.append(line)
    return '\n'.join(out_lines)

py_files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'strip_comments.py']
for f in py_files:
    with open(f, 'r', encoding='utf-8') as file:
        code = file.read()
    try:
        new_code = remove_comments(code)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_code)
        print(f"Stripped comments from {f}")
    except Exception as e:
        print(f"Error processing {f}: {e}")
