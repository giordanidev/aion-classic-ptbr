# TODO
# VERIFICAR SKILLS POR VERSÃO

import lxml.etree as parser
import os, time, codecs, shutil, zipfile, subprocess, sys
from pathlib import Path

print(f"+|+|+ SCRIPT INICIADO")
start_time_python = time.monotonic()
originais = ["data_eu", "Data_na"]
parsed = "_parsed"
downloads = "_arquivo"
versao_na = "280"
versao_eu = "200"
ignorar_parse = ["ui.xml", "msg.xml", "dialog.xml", "level.xml"]
arquivos = [
    "strings\\client_strings_ui.xml",
    "strings\\client_strings_msg.xml",
    "strings\\stringtable_dialog.xml",
    "strings\\client_strings_item.xml",
    "strings\\client_strings_item2.xml",
    "strings\\client_strings_skill.xml",
    "strings\\client_strings_level.xml"
]

def verificar_arquivos(contagem_arquivo, iteracoes, dest):
    print(f"[{contagem_arquivo}/{iteracoes}] Verificando arquivo: {dest}", end="\r")
    if os.path.isfile(dest):
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo existe: '{dest}' :: Removendo.", end="\r")
        os.remove(dest)
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo existe: '{dest}' :: Removido.")
    else:
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo não existe: '{dest}'.")
        if not os.path.isdir(os.path.dirname(dest)):
            print(f"[{contagem_arquivo}/{iteracoes}] Diretório não existe :: Criando diretório: '{os.path.dirname(dest)}'.", end="\r")
            os.makedirs(os.path.dirname(dest))
            print(f"[{contagem_arquivo}/{iteracoes}] Diretório não existe :: Diretório criado: '{os.path.dirname(dest)}'.")

def parsing():
    print(f">>>>> INICIANDO PARSE", end="\r")
    start_time_total = time.monotonic()

    arquivos_len = len(arquivos)
    iteracoes = arquivos_len*len(originais)

    print(f">>>>> INICIANDO PARSE :: {iteracoes} arquivos encontrados :: {len(originais)} iteração(ões) :: Total de {iteracoes} parses")

    for original in originais:

        print(f"##### ITERAÇÃO: {original}")
        start_time_original = time.monotonic()
        ignorar = False
        contagem_arquivo = 1
        for traducao in arquivos:
            for texto in traducao.split("_"):
                if texto in ignorar_parse:
                    ignorar = True

            start_time_traducao = time.monotonic()
            contagem = 0
            original_file = f"_originais\{original}\{traducao}"
            dest = f"{parsed}\{original}\{traducao}"
            print(f"[{contagem_arquivo}/{iteracoes}] Arquivo: {traducao}")

            original_tree = parser.parse(original_file)
            original_root = original_tree.getroot()
            original_len = len(original_root)

            traducao_tree = Path(traducao)
            traducao_root = parser.iterparse(traducao_tree, events=('start', 'end'))

            novo_parse = parser.Element('strings')

            start_time_line = time.monotonic()
            for original_string in original_root:
                texto_traducao = None
                if original_string.find('name') is not None:
                    if original_string.find('body') is not None:

                        for event, traducao_string in traducao_root:
                            if event == 'end':
                                if (traducao_string.tag == 'string'):
                                    if traducao_string.find('name') is not None:
                                        if traducao_string.find('body') is not None:
                                            
                                            if traducao_string.find('name').text == original_string.find('name').text:
                                                texto_traducao = traducao_string
                                                break

                if texto_traducao == None:
                    texto_traducao = original_string
                novo_string = parser.SubElement(novo_parse, texto_traducao.tag)
                
                for elemento in texto_traducao:
                    if ignorar == False:
                        if "DESC" in elemento.text.split("_"):
                            parser.SubElement(novo_string, elemento.tag).text = texto_traducao.find(elemento.tag).text
                        else:
                            parser.SubElement(novo_string, elemento.tag).text = original_string.find(elemento.tag).text
                    else:
                        parser.SubElement(novo_string, elemento.tag).text = texto_traducao.find(elemento.tag).text
            """
                execution_time = "%.2f" % (time.monotonic() - start_time_line)
                sys.stdout.write(f"[{contagem_arquivo}/{iteracoes}] Parsing: {str(contagem)}/{original_len} ({execution_time}s)", end="\r")
                contagem += 1
            print("")
            """
            
            verificar_arquivos(contagem_arquivo, iteracoes, dest)
            
            parser.ElementTree(novo_parse).write(dest, encoding='utf-8', xml_declaration=True, pretty_print=True)
            execution_time = "%.2f" % (time.monotonic() - start_time_traducao)
            print(f"[{contagem_arquivo}/{iteracoes}] Arquivo salvo em '{dest}' ({execution_time}s)")
            contagem_arquivo += 1

        execution_time = "%.2f" % (time.monotonic() - start_time_original)
        print(f"##### ITERAÇÃO FINALIZADA: {original} ({execution_time}s)")
        
    execution_time = "%.2f" % (time.monotonic() - start_time_total)
    print(f"!!!!! PARSE FINALIZADO ({execution_time}s)")

def unicode():
    print(f">>>> INICIANDO TRANSCRIÇÃO", end="\r")
    start_time_total = time.monotonic()
    arquivos.extend([
                "cutscene\\cs_ab1_001.xml", # não passar pelo parser
                "cutscene\\cs_ab1_002.xml" # não passar pelo parser
                ])

    contagem_arquivo = 1
    arquivos_len = len(arquivos)
    iteracoes = arquivos_len*len(originais)

    print(f">>>>> INICIANDO TRANSCRIÇÃO :: {iteracoes} arquivos encontrados :: {len(originais)} iteração(ões) :: Total de {iteracoes} transcrições")

    for original in originais:
        
        start_time_original = time.monotonic()
        print(f"##### ITERAÇÃO: {original}")

        for arquivo in arquivos:
            start_time_arquivo = time.monotonic()
            orig = f"{parsed}\{original}\{arquivo}"
            dest = f"PAK\z_{original}_ptBR\{arquivo}"

            verificar_arquivos(contagem_arquivo, iteracoes, dest)

            print(f"[{contagem_arquivo}/{iteracoes}] Copiando arquivo: '{orig}' -> '{dest}'", end="\r")
            if os.path.isfile(orig):
                shutil.copy2(orig, dest)
            else:
                shutil.copy2(f".\{arquivo}", dest)
            print(f"[{contagem_arquivo}/{iteracoes}] Copiando arquivo: '{orig}' -> '{dest}' :: Arquivo copiado")

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
            
            print(f"[{contagem_arquivo}/{iteracoes}] Transcrição finalizada", end="\r")

            f = open(dest, 'w', encoding='utf-8', newline='')
            f.write(contents)
            execution_time = "%.2f" % (time.monotonic() - start_time_arquivo)

            print(f"[{contagem_arquivo}/{iteracoes}] Transcrição finalizada :: Arquivo salvo ({execution_time}s)")
            contagem_arquivo += 1

        execution_time = "%.2f" % (time.monotonic() - start_time_original)
        print(f"##### ITERAÇÃO FINALIZADA: {original} ({execution_time}s)")

    execution_time = "%.2f" % (time.monotonic() - start_time_total)
    print(f"!!!!! TRANSCRIÇÃO FINALIZADA ({execution_time}s)")

def repack():
    start_time_total = time.monotonic()
    print(f">>>> INICIANDO REPACK")
    iteracoes = len(originais)
    contagem_arquivo = 1
    """
    # AGUARDANDO FIX DO DEV PARA ARQUIVOS COM NÚMEROS NO NOME!
    print(f"[{contagem_arquivo}/{iteracoes}] Gerando arquivo .PAK!", end="\r")
    subprocess.run([".\\Aion_Encdec.exe", "-r"])
    print(f"[{contagem_arquivo}/{iteracoes}] Gerando arquivo .PAK! :: Arquivo gerado")
    """
    for original in originais:
        start_time_original = time.monotonic()
        print(f"##### ITERAÇÃO: {original}")

        orig = f"REPACK\z_{original}_ptBR.pak"
        dest_temp = f"z_{original}_ptBR.pak"
        dest = f"{downloads}\z_{original}_ptBR.zip"

        verificar_arquivos(contagem_arquivo, iteracoes, dest)

        #COPIAR PAK PARA A PASTA TEMPORÁRIA PRINCIPAL PARA CRIAR O ZIP
        shutil.copy2(orig, dest_temp)
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo copiado: {dest_temp}")

        with zipfile.ZipFile(dest, 'w') as file:
            file.write(dest_temp)
        #with zipfile.ZipFile(zip_dest, 'r') as file:
        #    print(file.namelist())

        os.remove(dest_temp)
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo zip criado com sucesso: '{dest}'.")
        contagem_arquivo += 1

        execution_time = "%.2f" % (time.monotonic() - start_time_original)
        print(f"##### ITERAÇÃO FINALIZADA: {original} ({execution_time}s)")

    execution_time = "%.2f" % (time.monotonic() - start_time_total)
    print(f"!!!!! REPACK FINALIZADO ({execution_time}s)")

parsing()
#unicode()
#repack()

execution_time = "%.2f" % (time.monotonic() - start_time_python)
print(f"+|+|+ SCRIPT CONCLUÍDO ({execution_time}s)")