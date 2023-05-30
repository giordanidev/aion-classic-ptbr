import sys, os, codecs, shutil, subprocess

def encode():
    files = [
        "strings\\client_strings_ui.xml",
        "strings\\stringtable_dialog.xml",
        "cutscene\\cs_ab1_001.xml"
    ]

    for filename in files:
        orig = ".\\"+filename
        dest = ".\\PAK\\data_ptBR\\"+filename

        print(f"Verifying if file exists: {dest}")
        if os.path.isfile(dest):
            print("File exists, removing.")
            os.remove(dest)
            print("File removed.")
        else:
            print("File doesn't exists.")
        print(f"Copying orig: {orig} -> dest: {dest}")
        shutil.copy2(orig, dest)
        print("Copy success!")

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
        print("Replaced letters successfully!")

        f = open(filename, 'w', encoding='utf-8')
        f.write(contents)
        print("File saved successfully!")

    subprocess.check_call([r".\\Aion Encdec.exe", "-r data_ptBR.pak"])

    print("Repacked successfully!")

    orig_repack = ".\\REPACK\\data_ptBR.pak"
    dest_repack = "E:\\JOGOS\\aionclassic\\l10n\\ENG\\data\\data_ptBR.pak"
    dest_test = ".\\teste\\data_ptBR.pak"

    print(f"Installing orig_repack: {orig_repack} -> dest_repack: '{dest_repack}'")
    if os.path.isfile(dest_repack):
            os.remove(dest_repack)
    shutil.copy2(orig_repack, dest_repack)
    
    if os.path.isfile(dest_test):
            os.remove(dest_test)
    shutil.copy2(orig_repack, dest_test)

    print("Installed successfully!")

encode()