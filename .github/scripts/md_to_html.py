"""
Forge Style Guide — Markdown to HTML converter.

Produces HTML that renders correctly INSIDE a HubSpot page by using
inline styles on every element instead of relying on a <style> block.

Usage (CI):
    python .github/scripts/md_to_html.py README.md

Output: forge_style_guide_snippet.html (in repo root, consumed by publish-to-hubspot.js)
"""

import html as html_mod
import re
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: python md_to_html.py <input.md>")

with open(sys.argv[1], "r", encoding="utf-8") as f:
    md_text = f.read()

print(f"Read markdown from {sys.argv[1]} ({len(md_text)} chars)")

# ---------------------------------------------------------------------------
# Inline style constants
# ---------------------------------------------------------------------------
FONT = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif"
MONO_FONT = "ui-monospace, 'SFMono-Regular', 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

COLOR = "#171857"
BG = "#f8f8f8"

S_WRAPPER = f"text-align: left; color: {COLOR}; background-color: {BG}; font-family: {FONT}; line-height: 1.6; font-size: 16px; max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem;"
S_H3 = f"line-height: 1.25; color: {COLOR}; background-color: {BG}; font-family: {FONT}; font-size: 1.75em; font-weight: 600; margin: 0 0 0.75rem 0; padding: 0; border: none;"
S_H3_CENTERED = S_H3.replace("margin: 0 0 0.75rem 0", "margin: 0 0 0.75rem 0; text-align: center")
S_H5 = f"line-height: 1; color: {COLOR}; background-color: {BG}; font-family: {FONT}; font-size: 1.15em; font-weight: 600; margin: 1.75rem 0 0.5rem 0; padding: 0; border: none;"
S_P = f"color: {COLOR}; background-color: {BG}; font-family: {FONT}; font-size: 16px; line-height: 1.6; margin: 0.75rem 0; padding: 0;"
S_A = f"color: #0052CC; text-decoration: none;"
S_UL = f"text-align: left; padding-left: 1.5em; margin: 0.5rem 0; font-family: {FONT}; font-size: 16px; line-height: 1.6; color: {COLOR};"
S_LI = f"margin: 0.25rem 0; padding: 0; font-size: 16px; line-height: 1.6; color: {COLOR}; font-family: {FONT};"
S_HR = f"border: none; border-top: 1px solid #d1d9e0; margin: 2rem 0;"
S_CODE_WRAPPER = "margin: 1rem 0; border: 1px solid #d1d9e0; border-radius: 6px; overflow: hidden; text-align: left; background: #ffffff;"
S_CODE_HEADER = f"display: flex; align-items: center; padding: 8px 16px; background: #f6f8fa; border-bottom: 1px solid #d1d9e0; font-size: 12px; line-height: 1.5; color: #656d76; font-family: {FONT}; margin: 0;"
S_CODE_LANG = f"font-weight: 600; color: #1f2328; font-size: 12px; font-family: {FONT};"
S_PRE = f"margin: 0; padding: 16px; background: #ffffff; overflow-x: auto; font-size: 13.6px; line-height: 1.45; border: none; border-radius: 0; white-space: pre; word-wrap: normal;"
S_CODE = f"font-family: {MONO_FONT}; font-size: 13.6px; color: #1f2328; background: transparent; padding: 0; border: none; border-radius: 0; white-space: pre; word-break: normal; line-height: 1.45;"
S_INLINE_CODE = f"font-family: {MONO_FONT}; font-size: 0.85em; padding: 0.2em 0.4em; margin: 0 0.1em; background: #eff1f3; border-radius: 6px; color: #1f2328; border: none; white-space: nowrap;"
S_TABLE = "margin: 1rem 0; border-collapse: collapse; border: none; text-align: center;"
S_TD = f"padding: 0.5rem 1rem; text-align: center; vertical-align: top; border: none; background: transparent; font-family: {FONT}; color: {COLOR};"

HL = {
    "keyword": "color: #cf222e;",
    "type": "color: #0550ae;",
    "string": "color: #0a3069;",
    "comment": "color: #6e7781; font-style: italic;",
    "number": "color: #0550ae;",
    "builtin": "color: #8250df;",
    "tag": "color: #116329;",
    "attr": "color: #0550ae;",
    "decorator": "color: #8250df;",
    "variable": "color: #953800;",
    "flag": "color: #0550ae;",
    "punctuation": "color: #1f2328;",
}

# ---------------------------------------------------------------------------
# Image URL replacements 
# ---------------------------------------------------------------------------
IMAGE_REPLACEMENTS = {
    "./team/zishan-aslam.jpg": "https://raw.githubusercontent.com/valiantys-open-source/forge-style-guide/main/team/zishan-aslam.jpg",
    "./team/joshua-demetri.png": "https://raw.githubusercontent.com/valiantys-open-source/forge-style-guide/main/team/joshua-demetri.png",
    "./team/zachary-kipping.png": "https://raw.githubusercontent.com/valiantys-open-source/forge-style-guide/main/team/zachary-kipping.png",
    "./team/alisha-robinson.png": "https://raw.githubusercontent.com/valiantys-open-source/forge-style-guide/main/team/alisha-robinson.png",
    "./team/saurav-khatiwada.png": "https://raw.githubusercontent.com/valiantys-open-source/forge-style-guide/main/team/saurav-khatiwada.png",
}

LANG_DISPLAY = {
    "typescript": "TypeScript", "ts": "TypeScript", "tsx": "TypeScript",
    "javascript": "JavaScript", "js": "JavaScript", "jsx": "JSX",
    "yaml": "YAML", "yml": "YAML",
    "bash": "Bash", "sh": "Shell",
    "python": "Python", "py": "Python",
    "json": "JSON", "html": "HTML", "css": "CSS", "sql": "SQL",
}

TS_KEYWORDS = {
    "export", "async", "function", "const", "let", "var", "return",
    "if", "else", "switch", "case", "break", "default", "import", "from",
    "class", "new", "throw", "try", "catch", "finally", "await", "for",
    "while", "do", "of", "in", "typeof", "instanceof", "void", "delete",
    "this", "super", "extends", "implements", "interface", "type", "enum",
    "namespace", "module", "declare", "as", "is", "keyof", "readonly",
    "abstract", "static", "private", "protected", "public", "override",
    "satisfies", "using", "yield", "with",
}
TS_TYPES = {
    "string", "number", "boolean", "any", "void", "never", "unknown",
    "null", "undefined", "object", "symbol", "bigint", "Promise",
    "Array", "Map", "Set", "Record", "Partial", "Required", "Readonly",
    "true", "false",
}
YAML_KEYWORDS = {"true", "false", "null", "yes", "no", "on", "off"}
BASH_KEYWORDS = {
    "if", "then", "else", "elif", "fi", "for", "while", "do", "done",
    "case", "esac", "function", "return", "exit", "source", "export",
    "local", "readonly", "unset", "set", "shift",
}


def _esc(text): return html_mod.escape(text)
def _span(cls, text): return f'<span style="{HL.get(cls, "")}">{text}</span>'


def _highlight_ts(code):
    out = []; i = 0
    while i < len(code):
        if code[i:i+2] == '/*':
            end = code.find('*/', i+2); end = len(code) if end == -1 else end+2
            out.append(_span("comment", _esc(code[i:end]))); i = end; continue
        if code[i:i+2] == '//':
            end = code.find('\n', i)
            if end == -1: end = len(code)
            out.append(_span("comment", _esc(code[i:end]))); i = end; continue
        if code[i] == '`':
            j = i+1; r = _esc(code[i])
            while j < len(code) and code[j] != '`':
                if code[j:j+2] == '${':
                    d=1; k=j+2
                    while k<len(code) and d>0:
                        if code[k]=='{': d+=1
                        elif code[k]=='}': d-=1
                        k+=1
                    r += _esc(code[j:k]); j=k
                elif code[j]=='\\': r += _esc(code[j:j+2]); j+=2
                else: r += _esc(code[j]); j+=1
            if j<len(code): r += _esc(code[j]); j+=1
            out.append(_span("string", r)); i=j; continue
        if code[i] in ('"', "'"):
            q=code[i]; j=i+1
            while j<len(code) and code[j]!=q: j+=2 if code[j]=='\\' else 1
            if j<len(code): j+=1
            out.append(_span("string", _esc(code[i:j]))); i=j; continue
        if code[i]=='<' and i+1<len(code) and (code[i+1].isalpha() or code[i+1]=='/'):
            pk = i+(2 if code[i+1]=='/' else 1); te=pk
            while te<len(code) and (code[te].isalnum() or code[te] in '.-'): te+=1
            tn=code[pk:te]
            if tn and te<len(code) and code[te]=='>' and i>0 and (code[i-1].isalnum() or code[i-1] in '_$'):
                out.append(_esc('<')+_span("type",_esc(tn))+_esc('>')); i=te+1; continue
            j=i+1
            if code[j]=='/': j+=1
            while j<len(code) and (code[j].isalnum() or code[j] in '.-'): j+=1
            while j<len(code) and code[j]!='>': j+=1
            if j<len(code): j+=1
            tt=code[i:j]
            h=re.sub(r'(</?)([\w.-]+)', lambda m: _esc(m.group(1))+_span("tag",_esc(m.group(2))), tt)
            h=re.sub(r'(\w+)(=)', lambda m: _span("attr",_esc(m.group(1)))+_esc(m.group(2)), h)
            out.append(h); i=j; continue
        if code[i].isdigit() or (code[i]=='.' and i+1<len(code) and code[i+1].isdigit()):
            j=i
            while j<len(code) and (code[j].isalnum() or code[j] in '.xXeE_'): j+=1
            out.append(_span("number", _esc(code[i:j]))); i=j; continue
        if code[i].isalpha() or code[i] in '_$':
            j=i
            while j<len(code) and (code[j].isalnum() or code[j] in '_$'): j+=1
            w=code[i:j]
            if w in TS_KEYWORDS: out.append(_span("keyword", _esc(w)))
            elif w in TS_TYPES: out.append(_span("type", _esc(w)))
            elif w=="console": out.append(_span("builtin", _esc(w)))
            else: out.append(_esc(w))
            i=j; continue
        if code[i]=='@' and i+1<len(code) and (code[i+1].isalpha() or code[i+1]=='_'):
            j=i+1
            while j<len(code) and (code[j].isalnum() or code[j] in '_$'): j+=1
            out.append(_span("decorator", _esc(code[i:j]))); i=j; continue
        out.append(_esc(code[i])); i+=1
    return "".join(out)


def _highlight_yaml(code):
    lines=code.split('\n'); result=[]
    for line in lines:
        cm=re.match(r'^(\s*)(#.*)$', line)
        if cm: result.append(_esc(cm.group(1))+_span("comment",_esc(cm.group(2)))); continue
        kv=re.match(r'^(\s*)(- )?([\w./@-]+)(:)(.*)', line)
        if kv:
            indent,dash,key,colon,value=kv.groups(); p=_esc(indent)
            if dash: p+=_span("punctuation",_esc(dash))
            p+=_span("attr",_esc(key))+_esc(colon); value=value.strip()
            if value:
                p+=" "
                if value.startswith('"') or value.startswith("'"): p+=_span("string",_esc(value))
                elif value.lower() in YAML_KEYWORDS: p+=_span("keyword",_esc(value))
                elif re.match(r'^[\d.]+$', value): p+=_span("number",_esc(value))
                else: p+=_esc(value)
            result.append(p); continue
        lm=re.match(r'^(\s*)(- )(.*)', line)
        if lm:
            indent,dash,value=lm.groups(); p=_esc(indent)+_span("punctuation",_esc(dash))
            p+=_span("string",_esc(value)) if value.startswith(('"',"'")) else _esc(value)
            result.append(p); continue
        result.append(_esc(line))
    return "\n".join(result)


def _highlight_bash(code):
    lines=code.split('\n'); result=[]
    for line in lines:
        cm=re.match(r'^(\s*)(#.*)$', line)
        if cm: result.append(_esc(cm.group(1))+_span("comment",_esc(cm.group(2)))); continue
        out=[]; i=0
        while i<len(line):
            if line[i] in ('"',"'"):
                q=line[i]; j=i+1
                while j<len(line) and line[j]!=q: j+=2 if line[j]=='\\' else 1
                if j<len(line): j+=1
                out.append(_span("string",_esc(line[i:j]))); i=j; continue
            if line[i]=='$':
                j=i+1
                if j<len(line) and line[j]=='{':
                    end=line.find('}',j)
                    if end!=-1: out.append(_span("variable",_esc(line[i:end+1]))); i=end+1; continue
                while j<len(line) and (line[j].isalnum() or line[j]=='_'): j+=1
                out.append(_span("variable",_esc(line[i:j]))); i=j; continue
            if line[i]=='-' and i+1<len(line) and (line[i+1].isalpha() or line[i+1]=='-'):
                j=i+1
                if line[j]=='-': j+=1
                while j<len(line) and (line[j].isalnum() or line[j] in '-_'): j+=1
                out.append(_span("flag",_esc(line[i:j]))); i=j; continue
            if line[i].isalpha() or line[i]=='_':
                j=i
                while j<len(line) and (line[j].isalnum() or line[j] in '_-'): j+=1
                w=line[i:j]
                if w in BASH_KEYWORDS: out.append(_span("keyword",_esc(w)))
                elif i==0 or line[:i].strip()=='': out.append(_span("builtin",_esc(w)))
                else: out.append(_esc(w))
                i=j; continue
            out.append(_esc(line[i])); i+=1
        result.append("".join(out))
    return "\n".join(result)


def highlight_code(code, lang):
    ll = lang.lower() if lang else ""
    if ll in ("typescript","ts","tsx","javascript","js","jsx"): return _highlight_ts(code)
    elif ll in ("yaml","yml"): return _highlight_yaml(code)
    elif ll in ("bash","sh"): return _highlight_bash(code)
    else: return _esc(code)


# ---------------------------------------------------------------------------
# Markdown-to-HTML converter
# ---------------------------------------------------------------------------
HEADING_TAG_MAP  = {1: "h3", 2: "h5", 3: "h5", 4: "h6", 5: "h6", 6: "h6"}
HEADING_STYLE_MAP = {1: S_H3_CENTERED, 2: S_H5, 3: S_H5, 4: S_H5, 5: S_H5, 6: S_H5}


def _inline(text):
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" style="border-radius:4px;max-width:100%;height:auto;">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}" style="{S_A}">{m.group(1)}</a>', text)
    text = re.sub(r"\*{3}(.+?)\*{3}", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"_{3}(.+?)_{3}", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*{2}(.+?)\*{2}", r"<strong>\1</strong>", text)
    text = re.sub(r"_{2}(.+?)_{2}", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", lambda m: f'<code style="{S_INLINE_CODE}">{m.group(1)}</code>', text)
    return text


def convert(md):
    lines = md.splitlines(); html_parts = []; i = 0
    in_code_block = False; code_lang = ""; code_lines = []; para_lines = []

    def flush_para():
        if para_lines:
            text = " ".join(para_lines)
            html_parts.append(f'<p style="{S_P}">{_inline(text)}</p>')
            para_lines.clear()

    while i < len(lines):
        line = lines[i]
        if re.match(r"^\s*<!--.*-->\s*$", line): i+=1; continue

        fence = re.match(r"^```(\w*)", line)
        if fence:
            if not in_code_block:
                flush_para(); in_code_block=True; code_lang=fence.group(1); code_lines=[]
            else:
                raw = "\n".join(code_lines); hl = highlight_code(raw, code_lang)
                dl = LANG_DISPLAY.get(code_lang.lower(), code_lang.upper() if code_lang else "")
                hdr = f'<div style="{S_CODE_HEADER}"><span style="{S_CODE_LANG}">{_esc(dl)}</span></div>' if dl else ""
                html_parts.append(f'<div style="{S_CODE_WRAPPER}">{hdr}<pre style="{S_PRE}"><code style="{S_CODE}">{hl}</code></pre></div>')
                in_code_block = False
            i+=1; continue

        if in_code_block: code_lines.append(line); i+=1; continue

        if re.match(r"^\s*<(table|div|tr|td|img|br|hr|details|summary)", line, re.I):
            flush_para(); hb = []
            while i < len(lines):
                hb.append(lines[i])
                if (i+1 < len(lines) and lines[i+1].strip() == "" and not re.match(r"^\s*<", lines[i+1])):
                    i+=1; break
                i+=1
            else: i+=1
            html_parts.append("\n".join(hb)); continue

        hm = re.match(r"^(#{1,6})\s+(.*)", line)
        if hm:
            flush_para(); lvl=len(hm.group(1)); text=hm.group(2).strip()
            tag = HEADING_TAG_MAP.get(lvl, "h6"); style = HEADING_STYLE_MAP.get(lvl, S_H5)
            anchor = re.sub(r"[^a-z0-9\s-]", "", text.lower())
            anchor = re.sub(r"\s+", "-", anchor).strip("-")
            html_parts.append(f'<{tag} id="{anchor}" style="{style}">{_inline(text)}</{tag}>')
            i+=1; continue

        if re.match(r"^(\*{3,}|-{3,}|_{3,})\s*$", line):
            flush_para(); html_parts.append(f'<hr style="{S_HR}">'); i+=1; continue

        if re.match(r"^\s*[-*+]\s+", line):
            flush_para(); items = []
            while i < len(lines) and re.match(r"^\s*[-*+]\s+", lines[i]):
                it = re.sub(r"^\s*[-*+]\s+", "", lines[i])
                items.append(f'  <li style="{S_LI}">{_inline(it)}</li>'); i+=1
            html_parts.append(f'<ul style="{S_UL}">\n' + "\n".join(items) + "\n</ul>"); continue

        if re.match(r"^\s*\d+\.\s+", line):
            flush_para(); items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                it = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                items.append(f'  <li style="{S_LI}">{_inline(it)}</li>'); i+=1
            html_parts.append(f'<ol style="{S_UL}">\n' + "\n".join(items) + "\n</ol>"); continue

        if line.strip() == "": flush_para(); i+=1; continue
        para_lines.append(line.strip()); i+=1

    flush_para()
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Build output
# ---------------------------------------------------------------------------
body_html = convert(md_text)

for old_url, new_url in IMAGE_REPLACEMENTS.items():
    body_html = body_html.replace(old_url, new_url)

def _style_team_table(match):
    table_inner = match.group(1)
    first_tr = re.search(r'<tr>(.*?)</tr>', table_inner, re.DOTALL)
    num_cols = len(re.findall(r'<td>', first_tr.group(1))) if first_tr else 1
    col_width = round(100 / num_cols, 4)
    table_inner = re.sub(r'<td>', f'<td style="width: {col_width}%;">', table_inner)
    return f'<table id="teamTable" style="width: 100%; margin-left: auto; margin-right: auto;">\n<tbody>{table_inner}</tbody>\n</table>'

body_html = re.sub(r'<table id="teamTable">(.*?)</table>', _style_team_table, body_html, flags=re.DOTALL)

snippet_html = f'<div style="{S_WRAPPER}">\n{body_html}\n<p style="{S_P}">&nbsp;</p>\n</div>\n'

# Output to repo root so publish-to-hubspot.js can read it
snippet_path = "forge_style_guide_snippet.html"
with open(snippet_path, "w", encoding="utf-8") as f:
    f.write(snippet_html)

print(f"Snippet written to: {snippet_path} ({len(snippet_html):,} chars)")
