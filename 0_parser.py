import lxml.etree as parser
import shutil, os, time, math

arquivos = [
    #"strings\\client_strings_ui.xml",
    #"strings\\client_strings_msg.xml",
    #"strings\\stringtable_dialog.xml",
    "strings\\client_strings_item.xml",
    #"strings\\client_strings_item2.xml",
    #"strings\\client_strings_skill.xml",
    #"strings\\client_strings_level.xml"
]

originais = ["_data_eu\\", "_Data_na\\"]
#originais = ["_data_eu\\"]
parsed = "_parsed\\"

for traducao in arquivos:
    print(f"Arquivo: {traducao}")
    traducao_tree = parser.parse(traducao)
    traducao_root = traducao_tree.getroot()
    traducao_chunks_linhas = 5000

    total_chunks = math.ceil(len(traducao_root)/traducao_chunks_linhas)
    print(f"Lihas totais: {len(traducao_root)}")
    print(f"Número de chunks: {total_chunks}")

    linha_atual = 0
    linha_atual_total = 0
    linhas_total = len(traducao_root)-1
    linhas_restantes = linhas_total
    chunk_atual = 0
    traducao_chunks = {}
    traducao_chunks[chunk_atual] = []
    print(f"Criando chunk {chunk_atual} de {total_chunks}")
    for linha in traducao_root:
        if linha_atual_total <= linhas_total and linha_atual <= traducao_chunks_linhas:
            linhas_restantes = linhas_total - linha_atual_total
            print(f"Linha {linha_atual_total+1} de {linhas_total+1}- Linha chunk atual: {linha_atual+1} - Chunk atual: {chunk_atual+1} - Linhas restantes: {linhas_restantes} ", end="\r")
            traducao_chunks[chunk_atual].append(linha)
            
            linha_atual += 1
            linha_atual_total += 1
            if linha_atual == traducao_chunks_linhas:
                chunk_atual += 1
                linha_atual = 0
                traducao_chunks[chunk_atual] = []
                print("")
    print("")
    break
    for original in originais:
        start_time = time.monotonic()
        contagem = 0
        original = original+traducao
        dest = parsed+original

        print(f"Original: {original} \nFinal: {dest}")
        original_tree = parser.parse(original)
        original_root = original_tree.getroot()
        linhas_total = len(original_root)

        novo_parse = parser.Element(original_root.tag)

        for original_linha in original_root:
            novo_string = parser.SubElement(novo_parse, original_linha.tag)

            contagem += 1
            linha_nome = original_linha.find('name').text

            traducao_linha = traducao_root.find(f".//*[name='{linha_nome}']")
            
            if traducao_linha is not None:
                #print(linha_original, linha_original.find('id').text)
                if traducao_linha.find('body') is not None:
                    #print(linha_original.find('body').text)
                    if original_linha.find('body') is not None:
                        texto_traducao = original_linha.find('body').text
                    else:
                        texto_traducao = traducao_linha.find('body').text
                traducao_linha.getparent().remove(traducao_linha)
            #else:
                #print("Linha não encontrada!")
            
            for elemento in original_linha:
                if texto_traducao is not None:  
                    if (elemento.tag == 'body'):
                            parser.SubElement(novo_string, elemento.tag).text = texto_traducao
                            texto_traducao = None
                    else:
                        parser.SubElement(novo_string, elemento.tag).text = original_linha.find(elemento.tag).text
                else:
                    parser.SubElement(novo_string, elemento.tag).text = original_linha.find(elemento.tag).text

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
        #.indent(novo_parse, space="\t", level=0)
        print("============== Arquivo finalizado! ==============")