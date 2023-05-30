import sys
import codecs

def encode():
    files = [
        ".\\PAK\\data\\strings\\client_strings_ui.xml",
        ".\\PAK\\data\\strings\\stringtable_dialog.xml",
        ".\\PAK\\data\\cutscene\\cs_ab1_001.xml"
    ]
    #path = ".\\strings"
    #basename = "client_strings_ui_test.xml"
    #filename = path + "\\" + basename
    #file = open(filename, "rt")
    for filename in files:
        print(filename)
        f = codecs.open(filename, encoding='utf-8')
        contents = f.read()
        f.close

        char_unicode = {
            "º": "&ordm;",
            "ª": "&ordf;",
            "à": "&agrave;",
            "á": "&aacute;",
            "â": "&acirc;",
            "ã": "&atilde;",
            "ç": "&ccedil;",
            "é": "&eacute;",
            "ê": "&ecirc;",
            "í": "&iacute;",
            "ó": "&oacute;",
            "ô": "&ocirc;",
            "õ": "&otilde;",
            "ú": "&uacute;",
            "&apos;": "'",
            "´": "'",
            "`": "'"
        }

        contents="".join((char_unicode.get(x, x) for x in contents))

        f = open(filename, 'w', encoding='utf-8')
        f.write(contents)

encode()