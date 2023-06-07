import os,  shutil, subprocess

#print("Gerando arquivo .PAK!")
#Não está funcionando para o arquivo \strings\client_strings_item2.xml
#subprocess.call([r".\\Aion Encdec.exe", "-r", "data_ptBR.pak"])
#print("Arquivo .PAK gerado!")

orig_repack = ".\\REPACK\\data_ptBR.pak"
dest_repack = "E:\\JOGOS\\aionclassic\\l10n\\ENG\\data\\data_ptBR.pak"
dest_test = ".\\teste\\data_ptBR.pak"

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
    print("Arquivo de teste instalado com sucesso!")
except:
         print("ERRO! Não foi possível instalar.")