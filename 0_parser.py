import lxml.etree as parser
import os, time
from pathlib import Path

print(f">>>>> INICIANDO PARSE", end="\r")
start_time_total = time.monotonic()

arquivos = [
    "strings\\client_strings_ui.xml",
    "strings\\client_strings_msg.xml",
    "strings\\stringtable_dialog.xml",
    "strings\\client_strings_item.xml",
    "strings\\client_strings_item2.xml",
    "strings\\client_strings_skill.xml",
    "strings\\client_strings_level.xml"
]
arquivos_len = len(arquivos)

print(f">>>>> INICIANDO PARSE :: {arquivos_len} arquivos encontrados", end="\r")

originais = ["_data_eu", "_Data_na"]
#originais = ["_data_eu\\"]
parsed = "_parsed"

print(f">>>>> INICIANDO PARSE :: {arquivos_len} arquivos encontrados :: {len(originais)} iteração(ões) :: Total de {arquivos_len*len(originais)} parses", end="\r")
print("")

for original in originais:

    print(f">>>>> ITERAÇÃO: {original}")
    start_time_original = time.monotonic()

    contagem_arquivo = 1
    for traducao in arquivos:
        start_time_traducao = time.monotonic()
        contagem = 0
        original_file = original+"\\"+traducao
        dest = parsed+"\\"+original_file
        print(f"[{contagem_arquivo}/{arquivos_len}] Arquivo: {traducao}")

        original_tree = parser.parse(original_file)
        original_root = original_tree.getroot()
        original_len = len(original_root)

        traducao_tree = Path(traducao)
        traducao_root = parser.iterparse(traducao_tree, events=('start', 'end'))

        novo_parse = parser.Element('strings')

        start_time_line = time.monotonic()
        for original_string in original_root:
            texto_traducao = None
            #print(f"original_string.find('name') :: {original_string.find('name')}")
            if original_string.find('name') is not None:
                #print(f"original_string.find('body') :: {original_string.find('body')}")
                if original_string.find('body') is not None:

                    for event, traducao_string in traducao_root:
                        #print(f"event :: {event}")
                        if event == 'end':
                            #print(f"traducao_string.tag :: {traducao_string.tag}")
                            if (traducao_string.tag == 'string'):
                                #print(f"traducao_string.find('name') :: {traducao_string.find('name')}")
                                if traducao_string.find('name') is not None:
                                    #print(f"traducao_string.find('body') :: {traducao_string.find('body')}")
                                    if traducao_string.find('body') is not None:
                                        
                                        #print(f"traducao_string.find('name').text :: {traducao_string.find('name').text} || original_string.find('name').text :: {original_string.find('name').text}")
                                        if traducao_string.find('name').text == original_string.find('name').text:
                                            #print("FOUND ME!")
                                            texto_traducao = traducao_string
                                            #print(f"traducao_string.find('body').text: {traducao_string.find('body').text}")
                                            #traducao_string.clear()
                                            break

            #print(f"texto_traducao :: {texto_traducao}")
            if texto_traducao == None:
                texto_traducao = original_string
            novo_string = parser.SubElement(novo_parse, texto_traducao.tag)
            #print(f"novo_string :: {novo_string}")

            
            #print(f"texto_traducao :: {texto_traducao.find('name').text}")
            for elemento in texto_traducao:
                #print(f"elemento :: {elemento}")
                #print(f"texto_traducao.find(elemento.tag).text :: {texto_traducao.find(elemento.tag).text}")
                parser.SubElement(novo_string, elemento.tag).text = texto_traducao.find(elemento.tag).text

            execution_time = "%.2f" % (time.monotonic() - start_time_line)
            print(f"[{contagem_arquivo}/{arquivos_len}] Parsing: {str(contagem)}/{original_len} ({execution_time}s)", end="\r")
            contagem += 1
            #if contagem >= 4:
            #    break
        #break
        print("")

        print(f"[{contagem_arquivo}/{arquivos_len}] Verificando arquivo.", end="\r")
        if os.path.isfile(dest):
            print(f"[{contagem_arquivo}/{arquivos_len}] Verificando arquivo :: Arquivo existe :: Removendo", end="\r")
            os.remove(dest)
            print(f"[{contagem_arquivo}/{arquivos_len}] Verificando arquivo :: Arquivo existe :: Removido", end="\r")
        else:
            print(f"[{contagem_arquivo}/{arquivos_len}] Verificando arquivo :: Arquivo não existe.", end="\r")
            if not os.path.isdir(os.path.dirname(dest)):
                    print(f"[{contagem_arquivo}/{arquivos_len}] Verificando arquivo :: Arquivo não existe :: Diretório não existe :: Criando diretório", end="\r")
                    os.makedirs(os.path.dirname(dest))
                    print(f"[{contagem_arquivo}/{arquivos_len}] Verificando arquivo :: Arquivo não existe :: Diretório não existe :: Diretório criado", end="\r")
        print("")

        parser.ElementTree(novo_parse).write(dest, encoding='utf-8', xml_declaration=True, pretty_print=True)
        execution_time = "%.2f" % (time.monotonic() - start_time_traducao)
        print(f"[{contagem_arquivo}/{arquivos_len}] Arquivo salvo em '{dest}' ({execution_time}s)")
        contagem_arquivo += 1

    execution_time = "%.2f" % (time.monotonic() - start_time_original)
    print(f"##### ITERAÇÃO FINALIZADA: {original} ({execution_time}s)")
    
execution_time = "%.2f" % (time.monotonic() - start_time_total)
print(f"!!!!! SCRIPT FINALIZADO ({execution_time}s)")
