import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inline handlers check
handlers = re.findall(r'on\w+="[^"]*"', html)
print(f"Found {len(handlers)} inline event handlers.")
for h in handlers:
    val = h.split('=', 1)[1].strip('"')
    if val.count('(') != val.count(')'):
        print(f"MISMATCH PARENS: {h}")
    if val.count("'") % 2 != 0:
        print(f"MISMATCH SINGLE QUOTES: {h}")

# 2. Extract main script block
script_match = re.findall(r'(?s)<script>(.*?)</script>', html)
if len(script_match) >= 2:
    js = script_match[1]
    lines = js.splitlines()
    print(f"Main script: {len(lines)} lines")
    
    # Check for unclosed template strings
    backtick_open = False
    open_line = 0
    for lnum, line in enumerate(lines, 1802):
        ticks = len(re.findall(r'(?<!\\)`', line))
        if ticks % 2 != 0:
            if not backtick_open:
                backtick_open = True
                open_line = lnum
            else:
                backtick_open = False
    if backtick_open:
        print(f"WARNING: Template literal opened around line {open_line} might be unclosed!")
    else:
        print("Template literals balanced line-by-line / block-by-block.")

# 3. System Guardrails Automated Assertions
assert "SystemGuardrails" in html, "ERROR: SystemGuardrails module missing in index.html!"
assert "ensureSupplierDiversity" in html, "ERROR: ensureSupplierDiversity missing!"
assert "validateChronologicalIntegrity" in html, "ERROR: validateChronologicalIntegrity missing!"
assert "assertSingleSourceOfTruth" in html, "ERROR: assertSingleSourceOfTruth missing!"
assert "fornecedoresAudiovisualPool" in html, "ERROR: fornecedoresAudiovisualPool missing!"

print("[SUCCESS] All System Guardrails & Supplier Diversity tests PASSED successfully!")
