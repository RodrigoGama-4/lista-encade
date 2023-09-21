class BlocoDisco:
    def __init__(self, conteudo=None):
        self.conteudo = conteudo  # conteudo
        self.proximoBloco = None  # ponteiro

class SimulacaoDisco:
    def __init__(self, tamanho_disco):
        self.disco = [BlocoDisco() for _ in range(tamanho_disco)]  # instancia a quantidade de blocos dado pelo usuario
        self.blocosLivres = tamanho_disco  # Número inicial de blocos livres
        self.memoriaDisponivel = tamanho_disco  # Memória disponível inicialmente
        self.palavrasAdd = []

    def criarArquivo(self, nomeArquivo):
        if len(nomeArquivo) > self.memoriaDisponivel:  # Verifica se há memória suficiente para o arquivo
            print("Memória insuficiente para armazenar o arquivo.")
            return

        self.palavrasAdd.append(nomeArquivo)

        primeiroBloco = 0
        blocoAnterior = None
        primeiro_bloco_adicionado = False

        for letra in nomeArquivo:
          # Incrementa ate achar um bloco vazio
            while self.disco[primeiroBloco].conteudo is not None:
                primeiroBloco += 1

            self.disco[primeiroBloco].conteudo = letra   # adiciona a letra ao bloco
            if not primeiro_bloco_adicionado:
              self.palavrasAdd.append(primeiroBloco)
              primeiro_bloco_adicionado = True

            if blocoAnterior is not None:  # Atualiza o ponteiro do bloco anterior para apontar para o bloco atual
                self.disco[blocoAnterior].proximoBloco = primeiroBloco

            blocoAnterior = primeiroBloco
            primeiroBloco += 1

        self.memoriaDisponivel -= len(nomeArquivo)
        print(f"Arquivo '{nomeArquivo}' criado com sucesso.")
        self.mostrarConteudoBlocos()

    def lerArquivo(self, palavra):
        palavraEncontrada = False
        blocoInicial = None  # primeira letra da palavra
        palavraConcatenada = ""  #palavra concatenada

        # Encontrar o bloco onde a primeira letra da palavra foi encontrada
        for blocoIdx, bloco in enumerate(self.disco):
            if bloco.conteudo is not None and bloco.conteudo.startswith(palavra[0]):
                blocoInicial = blocoIdx
                break

        if blocoInicial is not None:
            # Começar a concatenar as letras dos blocos a partir do bloco inicial
            blocoAtual = blocoInicial
            while blocoAtual is not None:
                palavraConcatenada += self.disco[blocoAtual].conteudo
                blocoAtual = self.disco[blocoAtual].proximoBloco

            if palavraConcatenada == palavra:
                palavraEncontrada = True

        if palavraEncontrada:
            print(f"A palavra '{palavra}' está no disco.")
        else:
            print(f"A palavra '{palavra}' não está no disco.")

    def excluirArquivo(self, palavra):
      if palavra not in self.palavrasAdd:
          print(f"A palavra '{palavra}' não foi encontrada no Disco.")
          return

      # Encontra o índice do bloco onde a palavra começa
      indice_bloco = self.palavrasAdd.index(palavra)
      indice_bloco_encadeado = self.palavrasAdd[indice_bloco+1]

      # Remove a palavra da lista de palavras criadas
      self.palavrasAdd.pop(indice_bloco)  #remove a palavra
      self.palavrasAdd.pop(indice_bloco) #remove o indice

      # Remove a palavra da lista encadeada a partir do bloco indicado
      bloco_atual = indice_bloco_encadeado
      while bloco_atual is not None:
          self.disco[bloco_atual].conteudo = None
          proximoBloco = self.disco[bloco_atual].proximoBloco
          self.disco[bloco_atual].proximoBloco = None
          self.blocosLivres += 1
          self.memoriaDisponivel += 1
          bloco_atual = proximoBloco

      print(f"Arquivo '{palavra}' excluído com sucesso.")
      # Descomente a linha abaixo se desejar mostrar o conteúdo dos blocos após a exclusão
      self.mostrarConteudoBlocos()

    def mostrarConteudoBlocos(self):
        print("-----------Conteúdo dos blocos:----------------")
        for idx, bloco in enumerate(self.disco):
            if bloco.conteudo is not None:
                print(f"Bloco {idx}: {bloco.conteudo}", end=" -> ")

                if bloco.proximoBloco is not None:
                    print(f"Próximo Bloco: {bloco.proximoBloco}", end="")
                print()
