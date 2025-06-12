#!/usr/bin/env python3
import hashlib
import urllib.request
import ssl
import sys
from pathlib import Path

def gerar_hash_string(s: str, algoritmo: str = "md5") -> str:
    """
    Retorna o hash hexadecimal de string `s` usando o algoritmo `algoritmo`.
    """
    h = hashlib.new(algoritmo)
    h.update(s.encode("utf-8"))
    return h.hexdigest()

def gerar_hash_arquivo(caminho: Path, algoritmo: str = "md5") -> str:
    """
    Calcula o hash de um arquivo usando o algoritmo especificado.
    """
    h = hashlib.new(algoritmo)
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(8192), b""):
            h.update(bloco)
    return h.hexdigest()

def baixar_arquivo(url: str, destino: Path):
    """
    Faz o download do arquivo em `url` para o caminho `destino`.
    """
    try:
        # Criar contexto SSL que não verifica certificados (para resolver o erro SSL)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        # Usar urlopen com context e escrever manualmente
        with urllib.request.urlopen(url, context=ctx) as response:
            with destino.open('wb') as f:
                f.write(response.read())
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    print("Olá mundo!")
    # Exemplo de hash de string
    hash_str = gerar_hash_string("Olá mundo!")
    print(f"MD5 da string \"Olá mundo!\": {hash_str}\n")
    
    # Verificação de hash dos dois arquivos
    arquivo_original = Path("requests-2.32.4.tar.gz")
    arquivo_copia = Path("copia.tar.gz")
    esperado = "4a380c14fe0f4465c9dbf79ffacefd8f"
    
    print("=== VERIFICAÇÃO DE INTEGRIDADE ===\n")
    
    # Verificar arquivo original
    if arquivo_original.exists():
        hash_original = gerar_hash_arquivo(arquivo_original)
        print(f"MD5 do arquivo original ({arquivo_original.name}):")
        print(f"  Calculado: {hash_original}")
        print(f"  Esperado:  {esperado}")
        if hash_original == esperado:
            print("  Status: ✔️  Arquivo íntegro\n")
        else:
            print("  Status: ❌  Arquivo alterado\n")
    else:
        print(f"❌  Arquivo {arquivo_original.name} não encontrado\n")
    
    # Verificar arquivo cópia alterada
    if arquivo_copia.exists():
        hash_copia = gerar_hash_arquivo(arquivo_copia)
        print(f"MD5 da cópia alterada ({arquivo_copia.name}):")
        print(f"  Calculado: {hash_copia}")
        print(f"  Esperado:  {esperado}")
        if hash_copia == esperado:
            print("  Status: ✔️  Arquivo íntegro\n")
        else:
            print("  Status: ❌  Arquivo alterado\n")
            
        # Comparar os dois arquivos
        if arquivo_original.exists():
            if hash_original == hash_copia:
                print("🔍  Os dois arquivos são idênticos")
            else:
                print("🔍  Os dois arquivos são diferentes")
                print(f"     Diferença detectada nos hashes:")
                print(f"     Original: {hash_original}")
                print(f"     Cópia:    {hash_copia}")
    else:
        print(f"❌  Arquivo {arquivo_copia.name} não encontrado")

if __name__ == "__main__":
    main()