import lxml.etree as parser
import shutil, os, time

arquivos = [
    #"strings\\client_strings_ui.xml",
    #"strings\\client_strings_msg.xml",
    #"strings\\stringtable_dialog.xml",
    "strings\\client_strings_item.xml",
    #"strings\\client_strings_item2.xml",
    #"strings\\client_strings_skill.xml",
    #"strings\\client_strings_level.xml"
]

#originais = ["_data_eu\\", "_Data_na\\"]
originais = ["_data_eu\\"]
parsed = "_parsed\\"
novo_xml = "_novo\\"

for arquivo in arquivos:
    print(f"Arquivo: {arquivo}")
    arquivo_tree = parser.parse(arquivo)
    #print(arquivo_tree)
    arquivo_root = arquivo_tree.getroot()

    for original in originais:
        start_time = time.monotonic()
        contagem = 0
        original = original+arquivo
        dest = parsed+original
        print(f"Original: {original} \nFinal: {dest}")
        original_tree = parser.parse(original)
        original_root = original_tree.getroot()
        novo_arquivo = novo_xml+arquivo

        print(original_root.tag)
        novo_parse = parser.Element(original_root.tag)

        for linha in arquivo_root:
            #print(linha.tag)
            nova_string = parser.SubElement(novo_parse, linha.tag)
            #novo_texto = parser.SubElement(nova_string, linha.tag) # TODO - gerar todos os sub-elementos de texto com um laço "for"
            contagem += 1
            linhas_total = len(arquivo_root)
            linha_id = linha.find('id').text
            linha_nome = linha.find('name').text
            linha_body = linha.find('body').text
            #print(f"contagem: {contagem} - linha_id: {linha_id} - linha_nome: {linha_nome} - linha_body: {linha_body}")
            linha_original = original_root.find(f".//*[name='{linha_nome}']")
            if linha_original is not None:
                linha_original.find('body').text = linha_body
                linha_original.getparent().remove(linha_original)
            else: print("Linha não encontrada!")
            execution_time = "%.2f" % (time.monotonic() - start_time)
            print(f"Edição: {str(contagem)}/{str(linhas_total)} em {execution_time}s.", end="\r")
            if (contagem >= 20): # Número de linhas para testar!
                break
        print("")
    """

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
    """