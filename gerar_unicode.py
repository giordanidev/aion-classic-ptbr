import sys, os, codecs, shutil, subprocess

def encode():
    files = ["strings\\client_strings_ui.xml",
             "strings\\stringtable_dialog.xml",
             "cutscene\\cs_ab1_001.xml"]

    for filename in files:
        orig = ".\\"+filename
        dest = ".\\PAK\\data_ptBR\\"+filename

        print(f"Verificando se arquivo existe: {dest}")
        if os.path.isfile(dest):
            print("Arquivo existe, removendo.")
            os.remove(dest)
            print("Arquivo removido.")
        else:
            print("Arquivo não existe.")
            if not os.path.isdir(os.path.dirname(dest)):
                 print("Diretório não existe. Criando diretório.")
                 os.makedirs(os.path.dirname(dest))
                 print("Diretório criado.")

        print(f"Copiando orig: {orig} -> dest: {dest}")
        shutil.copy2(orig, dest)
        print("Copiado com sucesso!")

        f = codecs.open(dest, encoding='utf-8')
        contents = f.read()
        f.close

        char_unicode = {
            "º": "&ordm;", "ª": "&ordf;",
            "À": "&Agrave;", "Á": "&Aacute;", "Â": "&Acirc;", "Ã": "&Atilde;",
            "à": "&agrave;", "á": "&aacute;", "â": "&acirc;", "ã": "&atilde;",
            "Ç": "&Ccedil;",
            "ç": "&ccedil;",
            "É": "&Eacute;", "Ê": "&Ecirc;",
            "é": "&eacute;", "ê": "&ecirc;",
            "Í": "&Iacute;",
            "í": "&iacute;",
            "Ó": "&Oacute;", "Ô": "&Ocirc;", "Õ": "&Otilde;",
            "ó": "&oacute;", "ô": "&ocirc;", "õ": "&otilde;",
            "Ú": "&Uacute;",
            "ú": "&uacute;",
            "&apos;": "'", "´": "'", "`": "'"
        }

        contents="".join((char_unicode.get(x, x) for x in contents))
        print("Letras substituídas!")

        f = open(dest, 'w', encoding='utf-8')
        f.write(contents)
        print("Arquivo salvo!")

    print("Gerando arquivo .PAK!")
    subprocess.check_call([r".\\Aion Encdec.exe", "-r data_ptBR.pak"])

    print("Arquivo .PAK gerado!")

    orig_repack = ".\\REPACK\\data_ptBR.pak"
    dest_repack = "E:\\JOGOS\\aionclassic\\l10n\\ENG\\data\\data_ptBR.pak"
    dest_test = ".\\teste\\data_ptBR.pak"

    print(f"Instalando orig_repack: {orig_repack} -> dest_repack: '{dest_repack}'")
    print(f"Verificando se arquivo existe: {dest_repack}")
    if os.path.isfile(dest_repack):
        print(f"Arquivo existe. Removendo.")
        os.remove(dest_repack)
    else:
        if not os.path.isdir(os.path.dirname(dest_repack)):
            print("Diretório dest_repack não existe. Criando diretório.")
            os.makedirs(os.path.dirname(dest_repack))
            print("Diretório dest_repack criado.")
    shutil.copy2(orig_repack, dest_repack)

    print(f"Verificando se arquivo existe: {dest_test}")
    if os.path.isfile(dest_test):
            print(f"Arquivo existe. Removendo.")
            os.remove(dest_test)
    else:
        if not os.path.isdir(os.path.dirname(dest_test)):
            print("Diretório dest_test não existe. Criando diretório.")
            os.makedirs(os.path.dirname(dest_test))
            print("Diretório dest_test criado.")

    shutil.copy2(orig_repack, dest_test)

    print("Instalado com sucesso!")

encode()