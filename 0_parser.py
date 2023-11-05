import lxml.etree as parser
import shutil, os, time

arquivos = [
    "strings\\client_strings_ui.xml",
    #"strings\\client_strings_msg.xml",
    #"strings\\stringtable_dialog.xml",
    #"strings\\client_strings_item.xml",
    #"strings\\client_strings_item2.xml",
    #"strings\\client_strings_skill.xml",
    #"strings\\client_strings_level.xml"
]

#originais = ["_data_eu\\", "_Data_na\\"]
originais = ["_data_eu\\", "_Data_na\\"]
parsed = "_parsed\\"

for traducao in arquivos:
    print(f"Arquivo: {traducao}")
    traducao_tree = parser.parse(traducao)
    #print(arquivo_tree)
    traducao_root = traducao_tree.getroot()

    for original in originais:
        start_time = time.monotonic()
        contagem = 0
        original = original+traducao
        dest = parsed+original

        print(f"Original: {original} \nFinal: {dest}")
        original_tree = parser.parse(original)
        original_root = original_tree.getroot()

        #print(original_root.tag)
        novo_parse = parser.Element(original_root.tag)

        for traducao_linha in traducao_root:
            #print(traducao_linha.tag)
            novo_string = parser.SubElement(novo_parse, traducao_linha.tag)

            contagem += 1
            linhas_total = len(traducao_root)
            linha_nome = traducao_linha.find('name').text
            #print(linha_nome)
            
            linha_original = original_root.find(f".//*[name='{linha_nome}']")
            
            if linha_original is not None:
                #print(linha_original, linha_original.find('id').text)
                if linha_original.find('body') is not None:
                    #print(linha_original.find('body').text)
                    if traducao_linha.find('body') is not None:
                        texto_traducao = traducao_linha.find('body').text
                    else:
                        texto_traducao = linha_original.find('body').text
                linha_original.getparent().remove(linha_original)
            #else:
                #print("Linha não encontrada!")
            
            for elemento in traducao_linha:
                if (elemento.tag == 'body'):
                    if texto_traducao is not None:  
                        parser.SubElement(novo_string, elemento.tag).text = texto_traducao
                        texto_traducao = None
                    else:
                        parser.SubElement(novo_string, elemento.tag).text = traducao_linha.find(elemento.tag).text
                else:
                    parser.SubElement(novo_string, elemento.tag).text = traducao_linha.find(elemento.tag).text

            execution_time = "%.2f" % (time.monotonic() - start_time)
            print(f"Parsing: {str(contagem)}/{str(linhas_total)} em {execution_time}s.", end="\r")
            #if (contagem >= 10): # Número de linhas para testar!
            #    break
        print("")
        #print(parser.tostring(novo_parse, encoding='utf-8', xml_declaration=True, pretty_print=True))

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

        parser.ElementTree(novo_parse).indent(novo_parse, space="\t", level=0).write(dest, encoding='utf-8', xml_declaration=True, pretty_print=True)
        print("============== Arquivo finalizado! ==============")