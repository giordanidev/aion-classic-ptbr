import sys, os, codecs, shutil, subprocess

def encode():
    print("INICIANDO!")
    arquivos = [
                "strings\\client_strings_ui.xml",
                "strings\\client_strings_msg.xml",
                "strings\\stringtable_dialog.xml",
                "strings\\client_strings_item.xml",
                "strings\\client_strings_item2.xml",
                "strings\\client_strings_skill.xml",
                "strings\\client_strings_level.xml",
                "cutscene\\cs_ab1_001.xml", # não passar pelo parse
                "cutscene\\cs_ab1_002.xml" # não passar pelo parse
                ]

    for arquivo in arquivos:
        orig = ".\\"+arquivo
        dest = ".\\PAK\\data_ptBR\\"+arquivo

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
            "&apos;": "'", "´": "'", "`": "'", "’": "'", "‘": "'", " ": " ", "–": "-"
        }

        contents="".join((char_unicode.get(x, x) for x in contents))
        print("Letras substituídas!")

        f = open(dest, 'w', encoding='utf-8', newline='')
        f.write(contents)
        print("Arquivo salvo!")
        
    print("CONCLUÍDO!")

encode()