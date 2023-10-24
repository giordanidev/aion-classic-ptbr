import xml.etree.ElementTree as parser

arquivos = ["strings\\client_strings_ui.xml"
]

"""
arquivos = ["strings\\client_strings_ui.xml",
        "strings\\client_strings_msg.xml",
        "strings\\stringtable_dialog.xml",
        "strings\\client_strings_item.xml",
        "strings\\client_strings_item2.xml",
        "strings\\client_strings_skill.xml",
        "strings\\client_strings_level.xml"
]
"""

originais = "_originais\\"
contagem = 0

for arquivo in arquivos:
    original = originais+arquivo

    arquivo_tree = parser.parse(arquivo)
    arquivo_root = arquivo_tree.getroot()

    original_tree = parser.parse(original)
    original_root = original_tree.getroot()

    print("Arquivo: "+arquivo)
    for linha in arquivo_root:
        contagem += 1
        linhas_total = len(arquivo_root)
        print("Strings: "+str(contagem)+"/"+str(linhas_total), end="\r")
        linha_id = linha.find('id').text
        linha_nome = linha.find('name').text
        #print(contagem)
        #print(linha_id)
        #print(linha_nome)
        try:
            linha_body = linha.find('body').text
            #print(linha_body)

            linha_original = original_root.find(".//*[name='"+linha_nome+"']")
            linha_original.find('body').text = linha_body
        except: "" #print("ERRO! "+linha_id)
    print("")
    original_tree.write(original)