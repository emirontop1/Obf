import js
from pyscript import window
import random

def py_obfuscate(source_code):
    """
    Dosyadan gelen devasa veriyi kasma yapmadan 
    işleyen profesyonel LBI Obfuscator motoru.
    """
    if not source_code.strip():
        return "-- [Hata] Gönderilen kod boş!"
        
    # Büyük veriyi bellek dostu şekilde satırlara bölüyoruz
    lines = source_code.splitlines()
    bytecode = []
    string_pool = []
    
    # Rastgele Güvenlik Opcode'ları
    OP_PRINT = random.randint(100, 300)
    OP_EXEC = random.randint(400, 600)
    OP_RETURN = random.randint(700, 900)
    
    # Listeye ekleme hızını optimize etmek için yerel fonksiyon tanımları
    string_pool_append = string_pool.append
    bytecode_append = bytecode.append
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("--"):
            continue
            
        if line.startswith("print(") and line.endswith(")"):
            content = line[6:-1].strip('"\'')
            string_pool_append(content)
            bytecode_append(f"{{ {OP_PRINT}, {len(string_pool) - 1} }}")
        elif line.startswith("return"):
            string_pool_append(line)
            bytecode_append(f"{{ {OP_RETURN}, {len(string_pool) - 1} }}")
        else:
            string_pool_append(line)
            bytecode_append(f"{{ {OP_EXEC}, {len(string_pool) - 1} }}")
            
    # XOR Katmanı
    xor_key = random.randint(1, 255)
    encrypted_strings = []
    encrypted_strings_append = encrypted_strings.append
    
    for s in string_pool:
        lua_bytes = "".join(f"\\{ord(c) ^ xor_key:03d}" for c in s)
        encrypted_strings_append(f'"{lua_bytes}"')
        
    str_pool_data = ", ".join(encrypted_strings)
    bytecode_data = ", ".join(bytecode)
    
    # Nihai Güçlü MoonSec Tarzı VM Çıktısı
    vm_template = f"""--[[ 
    PRO LEVEL LUA VM OBFUSCATOR v2.5 (Large File Optimized)
    [XOR Key: {xor_key}] [Custom Opcodes Active]
]]
return (function(...)
    local _XOR_KEY = {xor_key}
    local _ENCRYPTED_POOL = {{ {str_pool_data} }}
    local _BYTECODE = {{ {bytecode_data} }}
    
    local _STR_POOL = {{}}
    for i = 1, #_ENCRYPTED_POOL do
        local s = _ENCRYPTED_POOL[i]
        local decrypted = ""
        for c in s:gmatch("\\\\%d%d%d") do
            local num = tonumber(c:sub(2))
            decrypted = decrypted .. string.char(bit32 and bit32.bxor(num, _XOR_KEY) or lshift and num ~ _XOR_KEY or num)
        end
        _STR_POOL[i] = decrypted
    end
    
    local _IP = 1
    local _VM_RUN = true
    
    while _VM_RUN and _IP <= #_BYTECODE do
        local inst = _BYTECODE[_IP]
        local opcode = inst[1]
        local arg = inst[2]
        
        if opcode == {OP_PRINT} then
            print(_STR_POOL[arg + 1])
        elseif opcode == {OP_EXEC} then
            local run = loadstring or load
            if run then
                run(_STR_POOL[arg + 1])()
            end
        elseif opcode == {OP_RETURN} then
            _VM_RUN = false
        end
        _IP = _IP + 1
    end
end)(...)"""

    return vm_template

# Köprüyü kur
window.py_obfuscate = py_obfuscate
try:
    window.setSystemReady()
except:
    pass
    
