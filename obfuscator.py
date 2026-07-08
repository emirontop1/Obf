import js
from pyscript import window

def py_obfuscate(source_code):
    """
    Tüm iş kodunun (Karıştırma Algoritmasının) döndüğü Python Alanı
    """
    if not source_code.strip():
        return "-- [Hata] Kod bos olamaz!"
        
    lines = source_code.split('\n')
    bytecode = []
    string_pool = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Basit Lexer yapısı: Print metotlarını yakalama
        if line.startswith("print(") and line.endswith(")"):
            content = line[6:-1].strip('"\'')
            string_pool.append(content)
            # Opcode 1 = Yazdırma Komutu
            bytecode.append(f"{{1, {len(string_pool) - 1}}}")
        else:
            # Diğer tüm genel script komutları için Raw komut çalıştırma havuzu
            string_pool.append(line)
            # Opcode 99 = Doğrudan Lua Yükleyici (load/loadstring)
            bytecode.append(f"{{99, {len(string_pool) - 1}}}")
            
    encrypted_strings = []
    for s in string_pool:
        # Metinleri ASCII bayt koduna (\xxx) çevirerek tarayıcıda koruma altına alma
        lua_bytes = "".join(f"\\{ord(c):03d}" for c in s)
        encrypted_strings.append(f'"{lua_bytes}"')
        
    str_pool_data = ", ".join(encrypted_strings)
    bytecode_data = ", ".join(bytecode)
    
    # Python tarafından üretilen nihai Lua Sanal Makinesi (VM) Yapısı
    vm_template = f"""--[[ v1.0.0 PyScript VM Obfuscator ]]
return(function(...)
    local _STR_POOL = {{ {str_pool_data} }}
    local _BYTECODE = {{ {bytecode_data} }}
    
    local _IP = 1
    local _VM_RUN = true
    
    local function w(idx) return _STR_POOL[idx + 1] end
    
    while _VM_RUN and _IP <= #_BYTECODE do
        local inst = _BYTECODE[_IP]
        local opcode = inst[1]
        local arg = inst[2]
        
        -- Sanal CPU Komut Seti Yürütücü (VM Interpreter)
        if opcode == 1 then
            print(w(arg))
        elseif opcode == 99 then
            local run = loadstring or load
            if run then
                run(w(arg))()
            end
        end
        _IP = _IP + 1
    end
end)(...)"""

    return vm_template

# Python fonksiyonunu JavaScript tarafında görünür kılıyoruz (Bridge Köprüsü)
window.py_obfuscate = py_obfuscate
try:
    window.setSystemReady()
except:
    pass
  
