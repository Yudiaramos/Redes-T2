import random
import math

# Variáveis globais
porcentagemDeErros = 0
enquadramento = 0
tipoDeControleDeErro = 0

def config():
    global porcentagemDeErros, enquadramento, tipoDeControleDeErro
    
    # Configurações iniciais do sistema
    porcentagemDeErros = int(input("Qual a porcentagem de erros do meio de comunicação? (Número inteiro entre 0 e 100): "))
    enquadramento = int(input("Enquadramento? (0 para contagem de caracteres, 1 para inserção de bytes): "))
    tipoDeControleDeErro = int(input("Detecção de erros? (0 para bit de paridade par, 1 para bit de paridade ímpar, 2 para CRC): "))

def meio_de_comunicacao(fluxo_bruto_de_bits):
    print("\nMeio de Comunicação:\n")
    print(f"Quadro original: {fluxo_bruto_de_bits}")
    
    fluxo_bruto_ponto_a = list(fluxo_bruto_de_bits)
    fluxo_bruto_ponto_b = []

    # Simulação do meio de comunicação, introduzindo erros
    for bit in fluxo_bruto_ponto_a:
        if random.randint(1, 100) > porcentagemDeErros:
            fluxo_bruto_ponto_b.append(bit)
        else:
            fluxo_bruto_ponto_b.append(1 - bit)

    print(f"Quadro após simulação de meio de comunicação: {fluxo_bruto_ponto_b}\n")

    # Próxima camada: Recebimento na Camada Física
    camada_fisica_receptora(fluxo_bruto_ponto_b)

def camada_fisica_receptora(quadro):
    print("\nCamada Física Receptora:\n")
    print("Recebendo...\n")

    # Próxima camada: Camada de Enlace de Dados
    camada_enlace_dados_receptora(quadro)

def camada_enlace_dados_receptora(quadro):
    print("\nCamada de Enlace Receptora:\n")
    print("Desenquadra e corrige erros...\n")

    # Controle de erro e desenquadramento
    quadro_corrigido = camada_enlace_dados_receptora_controle_de_erro(quadro)
    quadro_desenquadrado = camada_enlace_dados_receptora_enquadramento(quadro_corrigido)
    
    # Próxima camada: Camada de Aplicação Receptora
    camada_de_aplicacao_receptora(quadro_corrigido)

def camada_enlace_dados_receptora_enquadramento(quadro):
    print("\nDesenquadramento:\n")

    if enquadramento == 0:
        return camada_enlace_dados_receptora_enquadramento_contagem_de_caracteres(quadro)
    elif enquadramento == 1:
        return camada_enlace_dados_receptora_enquadramento_insercao_de_bytes(quadro)

def camada_enlace_dados_receptora_enquadramento_contagem_de_caracteres(quadro):
    print("Por Contagem de Caracteres:\n")
    print("Enquadrando...\n")
    return quadro[8:]

def camada_enlace_dados_receptora_enquadramento_insercao_de_bytes(quadro):
    print("Por Inserção de Bytes:\n")
    print("Desenquadrando...\n")
    
    byte_str = ""
    quadro_str = ""
    flag = "00001111"
    esc = "11110000"
    
    novo_quadro = []
    counter = 1
    ignore = False

    for bit in quadro:
        byte_str += str(bit)
        
        if counter == 8:
            if (byte_str == flag or byte_str == esc) and not ignore:
                ignore = True
            else:
                quadro_str += byte_str
                ignore = False

            counter = 0
            byte_str = ""
        counter += 1

    novo_quadro = [int(i) for i in quadro_str]
    return novo_quadro

def camada_enlace_dados_receptora_controle_de_erro(quadro):
    print("\nControle de Erro:\n")

    if tipoDeControleDeErro == 0:
        return camada_enlace_dados_receptora_controle_de_erro_bit_paridade_par(quadro)
    elif tipoDeControleDeErro == 1:
        return camada_enlace_dados_receptora_controle_de_erro_bit_paridade_impar(quadro)
    elif tipoDeControleDeErro == 2:
        return camada_enlace_dados_receptora_controle_de_erro_crc(quadro)

def camada_enlace_dados_receptora_controle_de_erro_bit_paridade_par(quadro):
    print("Por Bit de Paridade Par:\n")
    print("Corrigindo...\n")

    recebimento_paridade_par = quadro[:-1]
    paridade = sum(recebimento_paridade_par) % 2 == 0

    if quadro[-1] == paridade:
        print("\nRecebeu com sucesso!\n")
    else:
        print("\nProblema na comunicação detectado!\n")

    return recebimento_paridade_par

def camada_enlace_dados_receptora_controle_de_erro_bit_paridade_impar(quadro):
    print("Por Bit de Paridade Ímpar:\n")
    print("Corrigindo...\n")

    recebimento_paridade_impar = quadro[:-1]
    paridade = sum(recebimento_paridade_impar) % 2 == 1

    if quadro[-1] == paridade:
        print("\nRecebeu com sucesso!\n")
    else:
        print("\nProblema na comunicação detectado!\n")

    return recebimento_paridade_impar

def camada_enlace_dados_receptora_controle_de_erro_crc(quadro):
    print("Por CRC:\n")
    print("Inserindo correção...\n")

    polinomio_crc_32 = [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]
    mensagem = quadro[:-31]
    novo_quadro = list(quadro)
    valido = True

    for i in range(len(mensagem)):
        if novo_quadro[i] == 1:
            for j in range(27):
                novo_quadro[i + j] = novo_quadro[i + j] == polinomio_crc_32[j]

    for i in range(len(quadro)):
        if novo_quadro[i] != 0:
            valido = False

    if not valido:
        print("\nErro!\n")
    else:
        print("\nRecebeu com sucesso!\n")

    return mensagem

def camada_de_aplicacao_receptora(quadro):
    print("\nCamada de Aplicação Receptora:\n")
    print("Transferindo fluxo de bits para mensagem legível...\n")

    mensagem = decode_to_string(quadro)
    aplicacao_receptora(mensagem)
    
def decode_to_string(quadro):
    i = 0
    j = 0
    mensagem = ""

    while i < len(quadro):
        letra = 0
        for j in range(i, i + 8):
            if j < len(quadro):
                letra += quadro[j] * int(math.pow(2, 7 - (j - i)))

        mensagem += chr(letra)
        i += 8

    return mensagem

def aplicacao_receptora(mensagem):
    print("\nAplicação Receptora:\n")
    print(f"A mensagem recebida foi: {mensagem}\n")

def aplicacao_transmissora():
    print("\nInício:\n\n")
    config()
    mensagem = input("Digite uma mensagem: ")
    camada_de_aplicacao_transmissora(mensagem)

def camada_de_aplicacao_transmissora(mensagem):
    print("\nCamada de Aplicação Transmissora:\n")
    print(f"A mensagem original é: {mensagem}\n")
    
    # Próxima camada: Codificação para Bits
    quadro = encode_to_bits(mensagem)
    print(f"O quadro gerado é: {quadro}\n")
    
    # Próxima camada: Meio de Comunicação
    meio_de_comunicacao(quadro)

def encode_to_bits(mensagem):
    print("Codificando mensagem para bits...\n")
    bits = ''.join(format(ord(char), '08b') for char in mensagem)
    return [int(bit) for bit in bits]

# Função principal que inicia o processo de transmissão
aplicacao_transmissora()

