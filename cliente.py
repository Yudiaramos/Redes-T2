import random

# Variáveis globais
porcentagem_de_erros = 0
enquadramento = 0
tipo_de_controle_de_erro = 0

def config():
    global porcentagem_de_erros, enquadramento, tipo_de_controle_de_erro
    print("\nConfiguração:\n")
    porcentagem_de_erros = int(input("Qual a porcentagem de erros do meio de comunicação? (0 a 100): "))
    enquadramento = int(input("Qual vai ser o modo de enquadramento? (0 para contagem de caracteres, 1 para inserção de bytes): "))
    tipo_de_controle_de_erro = int(input("Qual vai ser o modo de detecção de erros? (0 para bit de paridade par, 1 para bit de paridade ímpar, 2 para CRC IEEE-802): "))

def meio_de_comunicacao(fluxo_bruto_de_bits):
    print("\nMeio de Comunicação:\n")
    print(f"Quadro original: {fluxo_bruto_de_bits}")
    
    fluxo_bruto_de_bits_ponto_a = list(fluxo_bruto_de_bits)
    fluxo_bruto_de_bits_ponto_b = []

    for bit in fluxo_bruto_de_bits_ponto_a:
        if random.randint(1, 100) > porcentagem_de_erros:
            fluxo_bruto_de_bits_ponto_b.append(bit)
        else:
            fluxo_bruto_de_bits_ponto_b.append(1 - bit)

    print(f"Quadro após o meio de comunicação: {fluxo_bruto_de_bits_ponto_b}")
    
    camada_fisica_receptora(fluxo_bruto_de_bits_ponto_b)

def camada_fisica_receptora(quadro):
    print("\nCamada Física Receptora:\n")
    print("Recebendo...\n")
    camada_enlace_dados_receptora(quadro)

def camada_enlace_dados_receptora(quadro):
    print("\nCamada de Enlace Receptora:\n")
    print("Desenquadrando e corrigindo erros...\n")
    quadro_corrigido = camada_enlace_dados_receptora_controle_de_erro(quadro)
    quadro_desenquadrado = camada_enlace_dados_receptora_enquadramento(quadro_corrigido)
    camada_de_aplicacao_receptora(quadro_corrigido)

def camada_enlace_dados_receptora_enquadramento(quadro):
    print("Desenquadramento: ")
    if enquadramento == 0:
        return camada_enlace_dados_receptora_enquadramento_contagem_de_caracteres(quadro)
    elif enquadramento == 1:
        return camada_enlace_dados_receptora_enquadramento_insercao_de_bytes(quadro)

def camada_enlace_dados_receptora_enquadramento_contagem_de_caracteres(quadro):
    print("por Contagem de Caracteres:\n")
    print("Enquadrando...\n")
    return quadro[8:]

def camada_enlace_dados_receptora_enquadramento_insercao_de_bytes(quadro):
    print("por Inserção de Bytes:\n")
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

    for i in quadro_str:
        novo_quadro.append(int(i))

    return novo_quadro

def camada_enlace_dados_receptora_controle_de_erro(quadro):
    print("Correção de Erros: ")
    if tipo_de_controle_de_erro == 0:
        return camada_enlace_dados_receptora_controle_de_erro_bit_paridade_par(quadro)
    elif tipo_de_controle_de_erro == 1:
        return camada_enlace_dados_receptora_controle_de_erro_bit_paridade_impar(quadro)
    elif tipo_de_controle_de_erro == 2:
        return camada_enlace_dados_receptora_controle_de_erro_crc(quadro)

def camada_enlace_dados_receptora_controle_de_erro_bit_paridade_par(quadro):
    print("por bit de paridade par:\n")
    print("Corrigindo...\n")

    recebimento_paridade_par = quadro[:-1]
    paridade = sum(recebimento_paridade_par) % 2 == 1

    if quadro[-1] == paridade:
        print("\nRecebeu com sucesso!\n")
    else:
        print("\nProblema na comunicação detectado!\n")

    return recebimento_paridade_par

def camada_enlace_dados_receptora_controle_de_erro_bit_paridade_impar(quadro):
    print("por bit de paridade ímpar:\n")
    print("Corrigindo...\n")

    recebimento_paridade_impar = quadro[:-1]
    paridade = sum(recebimento_paridade_impar) % 2 == 0  # Começa com falso para paridade ímpar

    if quadro[-1] == paridade:
        print("\nRecebeu com sucesso!\n")
    else:
        print("\nErro de paridade detectado!\n")

    return recebimento_paridade_impar

def camada_enlace_dados_receptora_controle_de_erro_crc(quadro):
    print("por CRC:\n")
    print("Inserindo correção...\n")

    # Implementação do algoritmo usando polinômio CRC-32 (IEEE 802)
    polinomio_crc_32 = [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]
    mensagem = quadro[:-31]
    novo_quadro = list(quadro)

    for i in range(len(mensagem)):
        if novo_quadro[i] == 1:
            for j in range(27):
                novo_quadro[i + j] = novo_quadro[i + j] == polinomio_crc_32[j]

    valido = all(bit == 0 for bit in novo_quadro)

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
    y = 0
    j = 0
    mensagem = ""
    letra = 0

    for i in range(0, len(quadro), 8):
        letra = 0
        y = 0
        for j in range(i, i + 8):
            if quadro[j] == 1:
                letra += pow(2, 7 - y)
            y += 1
        mensagem += chr(letra)

    return mensagem

def aplicacao_receptora(mensagem):
    print("\nAplicação Receptora:\n")
    print(f"A mensagem recebida foi: {mensagem}\n")

def main():
    print("\nInício:\n")
    config()
    # Simulação do envio de dados
    mensagem = input("Digite uma mensagem: ")
    fluxo_bruto_de_bits = [int(bit) for bit in ''.join(format(ord(char), '08b') for char in mensagem)]
    # Chamada da camada de enlace do transmissor
    meio_de_comunicacao(fluxo_bruto_de_bits)

if __name__ == "__main__":
    main()

