import xml.etree.ElementTree as parser
import shutil, os

arquivos = [
    #"strings\\client_strings_ui.xml",
    #"strings\\client_strings_msg.xml",
    "strings\\stringtable_dialog.xml",
    "strings\\client_strings_item.xml",
    "strings\\client_strings_item2.xml",
    "strings\\client_strings_skill.xml",
    "strings\\client_strings_level.xml"
]

#originais = ["_data_eu\\", "_Data_na\\"]
originais = ["_Data_na\\"]
parsed = "_parsed\\"

for arquivo in arquivos:
    print(f"Arquivo: {arquivo}")
    arquivo_tree = parser.parse(arquivo)
    arquivo_root = arquivo_tree.getroot()

    for original in originais:
        contagem = 0
        original = original+arquivo
        dest = parsed+original
        print(f"Original: {original} \nFinal: {dest}")
        original_tree = parser.parse(original)
        original_root = original_tree.getroot()

        for linha in arquivo_root:
            contagem += 1
            linhas_total = len(arquivo_root)
            print(f"Strings: {str(contagem)}/{str(linhas_total)}", end="\r")

            linha_id = linha.find('id').text
            linha_nome = linha.find('name').text
            #print(contagem)
            #print(linha_id)
            #print(linha_nome)
            try:
                linha_body = linha.find('body').text
                #print(linha_body)
                linha_original = original_root.find(f".//*[name='{linha_nome}']")
                linha_original.find('body').text = linha_body
            except: "" #print("ERRO! "+linha_id)
        print(f"Strings: {str(contagem)}/{str(linhas_total)} - COMPLETADO!", end="\r")
        print("")

        if os.path.isfile(dest):
            print("- Arquivo existe, removendo.")
            os.remove(dest)
            print("- Arquivo removido.")
        else:
            print("- Arquivo não existe.")
            if not os.path.isdir(os.path.dirname(dest)):
                    print("- Diretório não existe. Criando diretório.")
                    os.makedirs(os.path.dirname(dest))
                    print("- Diretório criado.")

        print(f"- Copiando original: {original} -> dest: {dest}")
        shutil.copy2(original, dest)
        print("- Copiado com sucesso!")

        original_tree.write(dest)
        print("============== Arquivo finalizado! ==============")