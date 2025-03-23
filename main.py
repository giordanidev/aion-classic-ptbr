#sys.exit()
import lxml.etree as parser
import os, time, codecs, shutil, zipfile, subprocess, sys, re
from pathlib import Path
from math import floor

print(f"+|+|+ SCRIPT INICIADO")
start_time_python = time.monotonic()
caminho_originais = ".\\_originais"
caminho_downloads = ".\\_download"
caminho_traduzidos = ".\\_traduzidos"
caminho_parsed = ".\\_parsed"
caminho_final = ".\\PAK"
data_jogo = "E:\\JOGOS\\Nova Aion\\l10n\\enu\\data\\z_nova_data_ptBR.pak"
ignorar_extencoes = [".html", ".htm"]

arquivos_originais = [name for name in os.listdir(caminho_originais) if os.path.isdir(os.path.join(caminho_originais, name))] #puxa os diretorios na pasta _originais
arquivos = []
for caminho, _, traduzir in os.walk(caminho_traduzidos):
    for arquivo in traduzir:
        arquivos.append(re.sub(caminho_traduzidos, '', os.path.join(caminho, arquivo))) #puxa o caminho completo de todos os arquivos já traduzidos
# Quando "ignorar_parse" for "Verdadeiro", o arquivo será transcrito por completo
# Usado em arquivos que os itens não tem um campo DESC
ignorar_parse = [
                ]
"""
                "ui.xml",
                "msg.xml",
                "dialog.xml",
                "level.xml",
                "samplemacro.xml"
"""
# Esses arquivos não devem passar pelo parse por serem HTML.
# Eles vão direto para a transcrição unicode e o repack.
nao_parse = [
            ]
"""
            "ui\\cleric_0.html",
            "ui\\cleric_1.html",
            "ui\\cleric_detail.html",
            "ui\\mage_0.html",
            "ui\\mage_1.html",
            "ui\\mage_detail.html",
            "ui\\scout_0.html",
            "ui\\scout_1.html",
            "ui\\scout_detail.html",
            "ui\\warrior_0.html",
            "ui\\warrior_1.html",
            "ui\\warrior_detail.html",
            "ui\\dark_desc_dimmed.html",
            "ui\\dark_desc.html",
            "ui\\light_desc_dimmed.html",
            "ui\\light_desc.html",
            "ui\\createinfos.html",
            "ui\\useragreement.html""
"""
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
    contagem_arquivo = 1
    arquivos_len = len(arquivos)
    iteracoes = arquivos_len*len(arquivos_originais)

    print(f">>>>> INICIANDO PARSE :: {iteracoes} arquivos encontrados :: {len(caminho_originais)} iteração(ões) :: Total de {iteracoes} parses")

    for original in arquivos_originais:

        print(f"##### ITERAÇÃO: {original}")
        start_time_original = time.monotonic()
        ignorar_parse_desc = False
        for traducao in arquivos:
            if verificarExtencao(arquivo) == True:
                print(f"[{contagem_arquivo}/{iteracoes}] Arquivo HTML: '{arquivo_traduzido}' :: Não passará pela transcrição")
                contagem_arquivo += 1
                continue

            for texto in traducao.split("_"):
                if texto in ignorar_parse:
                    ignorar_parse_desc = True

            start_time_traducao = time.monotonic()
            contagem = 0
            arquivo_original = f"{caminho_originais}\\{traducao}"
            arquivo_traduzido = f"{caminho_traduzidos}\\{traducao}"
            arquivo_parsed = f"{caminho_parsed}\\{traducao}"

            original_tree = parser.parse(arquivo_original)
            original_root = original_tree.getroot()
            original_len = len(original_root)

            traducao_tree = Path(arquivo_traduzido)
            traducao_root = parser.iterparse(traducao_tree, events=('start', 'end'))

            novo_parse = parser.Element('strings')

            start_time_line = time.monotonic()
            percentagem_anterior = 0
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
                    # Quando "ignorar_parse_desc" for "Verdadeiro", o arquivo será traduzido por completo
                    # Usado em arquivos que os itens não tem um campo DESC
                    if ignorar_parse_desc == False:
                        if "DESC" in elemento.text.split("_"):
                            parser.SubElement(novo_string, elemento.tag).text = texto_traducao.find(elemento.tag).text
                        else:
                            parser.SubElement(novo_string, elemento.tag).text = original_string.find(elemento.tag).text
                    else:
                        parser.SubElement(novo_string, elemento.tag).text = texto_traducao.find(elemento.tag).text
            # Contar as linhas gera um atraso na execução do script.
            
                execution_time = "%.2f" % (time.monotonic() - start_time_line)
                #sys.stdout.write(f"[{contagem_arquivo}/{iteracoes}] Parsing: {str(contagem)}/{original_len} ({execution_time}s)"+"\r")
                percentagem = floor((contagem_arquivo/iteracoes)*100)
                if percentagem > percentagem_anterior:
                    sys.stdout.write(f"Parsing: {str(contagem)}/{original_len} ({percentagem}%) ({execution_time}s)"+"\r")
                    percentagem_anterior = percentagem
                contagem += 1
            print("")
            
            verificar_arquivos(contagem_arquivo, iteracoes, arquivo_parsed)
            
            parser.ElementTree(novo_parse).write(arquivo_parsed, encoding='utf-8', xml_declaration=True, pretty_print=True)
            execution_time = "%.2f" % (time.monotonic() - start_time_traducao)
            print(f"[{contagem_arquivo}/{iteracoes}] Arquivo salvo em '{arquivo_parsed}' ({execution_time}s)")
            contagem_arquivo += 1

        execution_time = "%.2f" % (time.monotonic() - start_time_original)
        print(f"##### ITERAÇÃO FINALIZADA: {original} ({execution_time}s)")
        
    execution_time = "%.2f" % (time.monotonic() - start_time_total)
    print(f"!!!!! PARSE FINALIZADO ({execution_time}s)")

def unicode():
    print(f">>>> INICIANDO TRANSCRIÇÃO", end="\r")
    start_time_total = time.monotonic()
    arquivos.extend(nao_parse)

    contagem_arquivo = 1
    arquivos_len = len(arquivos)
    iteracoes = arquivos_len*len(arquivos_originais)

    print(f">>>>> INICIANDO TRANSCRIÇÃO :: {iteracoes} arquivos encontrados :: {len(arquivos_originais)} iteração(ões) :: Total de {iteracoes} transcrições")

    for original in arquivos_originais:
        
        start_time_original = time.monotonic()
        print(f"##### ITERAÇÃO: {original}")

        for arquivo in arquivos:
            start_time_arquivo = time.monotonic()
            arquivo_traduzido = f"{caminho_traduzidos}\\{arquivo}"
            arquivo_final = f"{caminho_final}\\{arquivo}"

            verificar_arquivos(contagem_arquivo, iteracoes, arquivo_final)

            print(f"[{contagem_arquivo}/{iteracoes}] Copiando arquivo: '{arquivo_traduzido}' -> '{arquivo_final}'", end="\r")
            if os.path.isfile(arquivo_traduzido):
                shutil.copy2(arquivo_traduzido, arquivo_final)
            else:
                shutil.copy2(f".\\{arquivo}", arquivo_final)
            print(f"[{contagem_arquivo}/{iteracoes}] Copiando arquivo: '{arquivo_traduzido}' -> '{arquivo_final}' :: Arquivo copiado")

            if verificarExtencao(arquivo) == True:
                print(f"[{contagem_arquivo}/{iteracoes}] Arquivo HTML: '{arquivo_traduzido}' :: Não passará pela transcrição")
                contagem_arquivo += 1
                continue

            f = codecs.open(arquivo_final, encoding='utf-8')
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

            print(f"[{contagem_arquivo}/{iteracoes}] Iniciando transcrição: '{arquivo_final}'")
            contents="".join((char_unicode.get(x, x) for x in contents))
            
            print(f"[{contagem_arquivo}/{iteracoes}] Transcrição finalizada", end="\r")

            f = open(arquivo_final, 'w', encoding='utf-8', newline='')
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
    iteracoes = len(arquivos_originais)
    contagem_arquivo = 1
    print(f"[{contagem_arquivo}/{iteracoes}] Gerando arquivo .PAK!", end="\r")
    subprocess.run([".\\Aion_Encdec13.exe", "-r"])
    print(f"[{contagem_arquivo}/{iteracoes}] Gerando arquivo .PAK! :: Arquivo gerado")
    for original in arquivos_originais:
        print(f"##### ITERAÇÃO: {original}")

        origem = f"REPACK\\{original}.pak"
        nome_pak = f"REPACK\\z_{original}_ptBR.pak"
        shutil.move(origem, nome_pak) # renomear o pak para o nome final
        pak_temp = f"z_{original}_ptBR.pak"
        destino_zip = f"{caminho_downloads}\\z_{original}_ptBR.zip"

        verificar_arquivos(contagem_arquivo, iteracoes, destino_zip)

        #COPIAR PAK PARA A PASTA TEMPORÁRIA PRINCIPAL PARA CRIAR O ZIP
        shutil.copy2(nome_pak, pak_temp)
        shutil.copy2(nome_pak, data_jogo)
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo copiado: {pak_temp}")

        with zipfile.ZipFile(destino_zip, 'w') as file:
            file.write(pak_temp)
        #with zipfile.ZipFile(zip_dest, 'r') as file:
        #    print(file.namelist())

        os.remove(pak_temp)
        print(f"[{contagem_arquivo}/{iteracoes}] Arquivo zip criado com sucesso: '{destino_zip}'.")
        contagem_arquivo += 1

        print(f"##### ITERAÇÃO FINALIZADA: {original}")

    execution_time = "%.2f" % (time.monotonic() - start_time_total)
    print(f"!!!!! REPACK FINALIZADO ({execution_time}s)")

def verificarExtencao(arquivo):
    if os.path.splitext(arquivo)[-1].lower() in ignorar_extencoes:
        return True
    else:
        return False
    
#parsing()
unicode()
repack()

execution_time = "%.2f" % (time.monotonic() - start_time_python)
print(f"+|+|+ SCRIPT CONCLUÍDO ({execution_time}s)")