import lxml.etree as parser
import shutil, os, time
from pathlib import Path

arquivos = [
    #"strings\\client_strings_ui.xml",
    #"strings\\client_strings_msg.xml",
    #"strings\\stringtable_dialog.xml",
    #"strings\\client_strings_item.xml",
    "strings\\client_strings_item2.xml",
    #"strings\\client_strings_skill.xml",
    #"strings\\client_strings_level.xml"
]

#originais = ["_data_eu\\", "_Data_na\\"]
originais = ["_data_eu\\"]
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
        #original_tree = parser.parse(original)
        #original_root = original_tree.getroot()
        original_tree = Path(original)
        original_root = parser.iterparse(original_tree, events=('start', 'end'))

        #print(original_root.tag)
        novo_parse = parser.Element('strings')

        for traducao_linha in traducao_root:
            #print(traducao_linha.tag)
            #novo_string = parser.SubElement(novo_parse, traducao_linha.tag)

            contagem += 1
            linhas_total = len(traducao_root)
            linha_nome = traducao_linha.find('name').text
            #print(linha_nome)

            linha_original = None
            texto_traducao = None

            #print(f"contagem: {contagem} - linha_id: {linha_id} - linha_nome: {linha_nome} - linha_body: {linha_body}")
            
            for event, element in original_root:
                if event == 'end':
                    #print(element.tag)
                    if (element.tag == 'string'):
                        novo_string = parser.SubElement(novo_parse, element.tag)
                        if element.find('name') is not None:
                            if linha_nome != element.find('name').text:
                                print("NAY!")
                        
                            element.getparent().remove(element)
                            break

            #for original_linha in original_root:
            #    print(original_linha.find('name').text)
            #    if original_linha.find('name').text == linha_nome:
            #        linha_original = original_linha
            #        break

            #print(f"contagem: {contagem} - linha_id: {linha_id} - linha_nome: {linha_nome} - linha_body: {linha_body}")
            #linha_original = original_root.find(f".//*[name='{linha_nome}']")
            
            if linha_original is not None:
                #print(linha_original, linha_original.find('id').text)
                if linha_original.find('body') is not None:
                    #print(linha_original.find('body').text)
                    if traducao_linha.find('body') is not None:
                        texto_traducao = traducao_linha.find('body').text
                    else:
                        texto_traducao = linha_original.find('body').text
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

            #linha_original.getparent().remove(linha_original)

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

        parser.ElementTree(novo_parse).write(dest, encoding='utf-8', xml_declaration=True, pretty_print=True)
        print("============== Arquivo finalizado! ==============")