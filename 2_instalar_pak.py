import os, shutil, subprocess, zipfile

orig_repack_eu = ".\\REPACK\\data_eu_ptBR.pak"
dest_repack_eu = ".\\arquivo\\data_eu_ptBR.pak"
dest_zip_eu = ".\\arquivo\\data_eu_ptBR.zip"

orig_repack_na = ".\\REPACK\\data_na_ptBR.pak"
dest_repack_na = ".\\arquivo\\data_na_ptBR.pak"
dest_zip_na = ".\\arquivo\\data_na_ptBR.zip"

# TODO
# ARRUMAR TUDO!

print(f"Instalando orig_repack: {orig_repack} -> dest_repack: '{dest_repack}'")
print(f"Verificando se arquivo existe: {dest_repack}")
if os.path.isfile(dest_repack):
    try:
        print(f"Arquivo existe. Removendo.")
        os.remove(dest_repack)
    except:
         print("ERRO! Não foi possível remover.")
else:
    if not os.path.isdir(os.path.dirname(dest_repack)):
        print("Diretório dest_repack não existe. Criando diretório.")
        os.makedirs(os.path.dirname(dest_repack))
        print("Diretório dest_repack criado.")
try:
    shutil.copy2(orig_repack, dest_repack)
    print(f"Arquivo copiado: {dest_repack}")
except:
         print("ERRO! Não foi possível copiar.")

print(f"Verificando se arquivo existe: {dest_test}")
if os.path.isfile(dest_test):
    try:
        print(f"Arquivo existe. Removendo.")
        os.remove(dest_test)
    except:
        print("ERRO! Não foi possível remover.")
else:
    if not os.path.isdir(os.path.dirname(dest_test)):
        print("Diretório dest_test não existe. Criando diretório.")
        os.makedirs(os.path.dirname(dest_test))
        print("Diretório dest_test criado.")
try:
    shutil.copy2(orig_repack, dest_test)
    shutil.copy2(orig_repack, ".\\data_ptBR.pak")
    print("Arquivo de teste instalado com sucesso!")
except:
         print("ERRO! Não foi possível instalar.")
try:
    with zipfile.ZipFile(zip_test, 'w') as file:
        file.write(".\\data_ptBR.pak")
    with zipfile.ZipFile(zip_test, 'r') as file:
        print(file.namelist())
    os.remove(".\\data_ptBR.pak")
    print("Arquivo zip criado com sucesso!")
except:
         print("Não foi possível criar o arquivo zip.")