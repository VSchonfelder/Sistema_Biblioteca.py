import csv
from datetime import datetime, timedelta

class Livro:
    def __init__(self, titulo, autores, edicao, exemplares):
        self.titulo = titulo
        self.autores = autores
        self.edicao = edicao
        self.exemplares = exemplares
        self.disponiveis = exemplares
    
    def alocar(self):
        if self.disponiveis > 0:
            self.disponiveis -= 1
            return True
        return False
    
    def devolver(self):
        self.disponiveis += 1


class Membro:
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome
        self.pertence_instituicao = True


class Emprestimo:
    def __init__(self, livro, membro, data_locacao):
        self.livro = livro
        self.membro = membro
        self.data_locacao = data_locacao
        self.data_devolucao_prevista = data_locacao + timedelta(days=15)
        self.data_devolucao_real = None
        self.multa = 0.0
    
    def devolver(self, data_devolucao):
        self.data_devolucao_real = data_devolucao
        if self.data_devolucao_real > self.data_devolucao_prevista:
            dias_atraso = (self.data_devolucao_real - self.data_devolucao_prevista).days
            self.multa = dias_atraso * 10.0
        self.livro.devolver()


class Biblioteca:
    def __init__(self):
        self.livros = {}
        self.membros = {}
        self.emprestimos_ativos = []
        self.historico_emprestimos = []
    
    def carregar_livros(self, caminho_csv):
        with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                livro = Livro(row['titulo'], row['autores'], int(row['edicao']), int(row['quantidade']))
                self.adicionar_livro(livro)
    
    def carregar_membros(self, caminho_csv):
        with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                membro = Membro(row['matricula'], row['nome'])
                self.adicionar_membro(membro)

    def adicionar_livro(self, livro):
        self.livros[livro.titulo] = livro
    
    def adicionar_membro(self, membro):
        self.membros[membro.matricula] = membro
    
    def alocar_livro(self, matricula_membro, titulo_livro, data_locacao):
        membro = self.membros.get(matricula_membro)
        livro = self.livros.get(titulo_livro)
        
        if not membro:
            print(f"Membro com matrícula {matricula_membro} não encontrado.\n")
            return
        
        if livro and livro.alocar():
            emprestimo = Emprestimo(livro, membro, data_locacao)
            self.emprestimos_ativos.append(emprestimo)
            print(f"Livro '{titulo_livro}' alocado com sucesso para {membro.nome}.\n")
        else:
            print(f"Livro '{titulo_livro}' indisponível.\n")
    
    def devolver_livro(self, matricula_membro, titulo_livro, data_devolucao):
        emprestimo = next((e for e in self.emprestimos_ativos if e.livro.titulo == titulo_livro and e.membro.matricula == matricula_membro), None)
        
        if emprestimo:
            emprestimo.devolver(data_devolucao)
            self.emprestimos_ativos.remove(emprestimo)
            self.historico_emprestimos.append(emprestimo)
            print(f"\n\nLivro '{titulo_livro}' devolvido com sucesso.\n")
            if emprestimo.multa > 0:
                print(f"Atraso detectado. Multa aplicada: R$ {emprestimo.multa:.2f}\n")
        else:
            print(f"Empréstimo do livro '{titulo_livro}' não encontrado.\n")
    
    def gerar_relatorio(self, data_inicio, data_fim):
        total_multas = 0.0
        total_atrasos = 0
        
        print(f"\n\nRelatório de {data_inicio} até {data_fim}:\n")
        for emprestimo in self.historico_emprestimos:
            if data_inicio <= emprestimo.data_locacao <= data_fim:
                print(f"Membro: {emprestimo.membro.nome} - Livro: {emprestimo.livro.titulo}\n")
                if emprestimo.multa > 0:
                    total_atrasos += 1
                    total_multas += emprestimo.multa
        
        print(f"Total de atrasos: {total_atrasos}")
        print(f"Total em multas: R$ {total_multas:.2f}")



biblioteca = Biblioteca()


biblioteca.carregar_livros('livros.csv')
biblioteca.carregar_membros('membros.csv')


data_locacao = datetime(2024, 10, 1)
biblioteca.alocar_livro("20230019", "O Nome da Rosa", data_locacao)
biblioteca.alocar_livro("20230002", "O Nome da Rosa", data_locacao)
biblioteca.alocar_livro("20230052", "Dom Quixote", data_locacao)

data_locacao = datetime(2024, 10, 2)
biblioteca.alocar_livro("20230070", "As Flores do Mal", data_locacao)
biblioteca.alocar_livro("20230084", "1984", data_locacao)
biblioteca.alocar_livro("20230010", "As Vinhas da Ira", data_locacao)
biblioteca.alocar_livro("20230012", "O Som e a Fúria", data_locacao)

data_locacao = datetime(2024, 10, 3)
biblioteca.alocar_livro("20230013", "O Pequeno Príncipe", data_locacao)
biblioteca.alocar_livro("20230022", "A Metamorfose", data_locacao)
biblioteca.alocar_livro("20230023", "A Glória Eterna", data_locacao)

data_locacao = datetime(2024, 10, 4)
biblioteca.alocar_livro("20231902", "O Pequeno Príncipe", data_locacao)
biblioteca.alocar_livro("20230095", "O Segundo Sexo", data_locacao)
biblioteca.alocar_livro("20230099", "A Peste", data_locacao)
biblioteca.alocar_livro("20230008", "Os Miseráveis", data_locacao)

data_locacao = datetime(2024, 10, 5)
biblioteca.alocar_livro("20230058", "O Jogo da Amarelinha", data_locacao)
biblioteca.alocar_livro("20230062", "O Segundo Sexo", data_locacao)
biblioteca.alocar_livro("20230070", "A Montanha Mágica", data_locacao)
biblioteca.alocar_livro("20230094", "O Mestre e Margarida", data_locacao)
biblioteca.alocar_livro("20230002", "A Hora da Estrela", data_locacao)



data_devolucao = datetime(2024, 10, 20)
biblioteca.devolver_livro("20230084", "1984", data_devolucao)
biblioteca.devolver_livro("20230094", "O Mestre e Margarida", data_devolucao)
biblioteca.devolver_livro("20230009", "Angústia", data_devolucao)
biblioteca.devolver_livro("20230008", "Os Miseráveis", data_devolucao)

data_devolucao = datetime(2024, 10, 19)
biblioteca.devolver_livro("20230095", "O Segundo Sexo", data_devolucao)
biblioteca.devolver_livro("20230002", "A Hora da Estrela", data_devolucao)
biblioteca.devolver_livro("20230070", "A Montanha Mágica", data_devolucao)
biblioteca.devolver_livro("20230058", "O Jogo da Amarelinha", data_devolucao)

data_devolucao = datetime(2024, 10, 18)
biblioteca.devolver_livro("20230099", "A Peste", data_devolucao)
biblioteca.devolver_livro("20230062", "O Segundo Sexo", data_devolucao)
biblioteca.devolver_livro("20230012", "O Som e a Fúria", data_devolucao)
biblioteca.devolver_livro("20230022", "A Metamorfose", data_devolucao)

data_devolucao = datetime(2024, 10, 17)
biblioteca.devolver_livro("20230013", "O Pequeno Príncipe", data_devolucao)
biblioteca.devolver_livro("20230019", "O Nome da Rosa", data_devolucao)
biblioteca.devolver_livro("20230052", "Dom Quixote", data_devolucao)
biblioteca.devolver_livro("20230010", "As Vinhas da Ira", data_devolucao)

data_devolucao = datetime(2024, 10, 16)
biblioteca.devolver_livro("20230070", "As Flores do Mal", data_devolucao)
biblioteca.devolver_livro("20230002", "O Nome da Rosa", data_devolucao)


data_inicio = datetime(2024, 10, 1)
data_fim = datetime(2024, 10, 20)
biblioteca.gerar_relatorio(data_inicio, data_fim)