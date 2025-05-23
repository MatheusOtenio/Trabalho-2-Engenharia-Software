import csv
import os

ARQUIVO_CSV = os.path.join(os.path.dirname(__file__), "usuarios.csv")

class Notificacao:
    def __init__(self, mensagem, lida=False):
        self.mensagem = mensagem
        self.lida = lida

class Grupo:
    def __init__(self, materia):
        self.materia = materia
        self.membros = []

    def adicionar_membro(self, perfil):
        if perfil not in self.membros:
            self.membros.append(perfil)
            perfil.notificacoes.append(Notificacao(f"Você foi adicionado ao grupo de '{self.materia}'."))
            for m in self.membros:
                if m != perfil:
                    m.notificacoes.append(Notificacao(f"{perfil.nome} entrou no grupo de '{self.materia}'."))

class Perfil:
    def __init__(self, nome, ra, email, materias=None, amigos=None, grupos=0):
        self.nome = nome
        self.ra = ra
        self.email = email
        self.materias_interesse = materias if materias else []
        self.amigos = amigos if amigos else []
        self.grupos_participados = grupos
        self.notificacoes = []

    def mostrar_dashboard(self, sistema):
        print(f"\n📊 DASHBOARD DE {self.nome.upper()}")
        print(f"🆔 RA: {self.ra}")
        print(f"📧 Email: {self.email}")
        print(f"📘 Matérias de interesse: {', '.join(self.materias_interesse) if self.materias_interesse else 'Nenhuma'}")
        print("👥 Amigos:")
        if self.amigos:
            for ra in self.amigos:
                amigo = sistema.buscar_usuario(ra)
                if amigo:
                    print(f"  - {amigo.nome} ({ra}) | Email: {amigo.email}")
        else:
            print("  Nenhum amigo adicionado.")
        print(f"🧩 Grupos participados: {self.grupos_participados}")
        print(f"🔔 Notificações não lidas: {sum(1 for n in self.notificacoes if not n.lida)}")
        print("-" * 40)

    def salvar(self, todos):
        for i, u in enumerate(todos):
            if u.ra == self.ra:
                todos[i] = self
                break
        else:
            todos.append(self)

        with open(ARQUIVO_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ra", "nome", "email", "materias", "amigos", "grupos"])
            for u in todos:
                writer.writerow([
                    u.ra,
                    u.nome,
                    u.email,
                    ";".join(u.materias_interesse),
                    ";".join(u.amigos),
                    u.grupos_participados
                ])

    def adicionar_materia(self, materia, sistema):
        if materia not in self.materias_interesse:
            self.materias_interesse.append(materia)
            sistema.adicionar_usuario_ao_grupo(self, materia)

    def adicionar_amigo(self, ra_amigo, sistema):
        if ra_amigo == self.ra:
            print("⚠️ Você não pode se adicionar como amigo.")
            return

        if ra_amigo in self.amigos:
            print("ℹ️ Esse usuário já está na sua lista de amigos.")
            return

        amigo = sistema.buscar_usuario(ra_amigo)
        if not amigo:
            print("❌ RA não encontrado no sistema.")
            return

        self.amigos.append(ra_amigo)
        if self.ra not in amigo.amigos:
            amigo.amigos.append(self.ra)
        print(f"✅ {amigo.nome} agora é seu amigo!")

        self.salvar(sistema.usuarios)
        amigo.salvar(sistema.usuarios)

    def remover_amigo(self, ra_amigo, sistema):
        if ra_amigo in self.amigos:
            self.amigos.remove(ra_amigo)
            amigo = sistema.buscar_usuario(ra_amigo)
            if amigo and self.ra in amigo.amigos:
                amigo.amigos.remove(self.ra)
                amigo.salvar(sistema.usuarios)
            print(f"👋 Amizade com {ra_amigo} removida.")
        else:
            print("⚠️ RA não está na sua lista de amigos.")
        self.salvar(sistema.usuarios)

    def ver_amigos(self, sistema):
        while True:
            print("\n👥 LISTA DE AMIGOS:")
            if not self.amigos:
                print("Você ainda não tem amigos adicionados.")
            else:
                for ra in self.amigos:
                    amigo = sistema.buscar_usuario(ra)
                    if amigo:
                        print(f"- {amigo.nome} ({ra}) | Email: {amigo.email}")
                    else:
                        print(f"- RA {ra} (não encontrado)")

            print("\n1. Adicionar amigo")
            print("2. Remover amigo")
            print("3. Ver matérias em comum")
            print("0. Voltar")

            op = input("Escolha uma opção: ").strip()

            if op == "1":
                ra_novo = input("RA do novo amigo: ").strip()
                self.adicionar_amigo(ra_novo, sistema)
            elif op == "2":
                ra_remover = input("RA do amigo a remover: ").strip()
                self.remover_amigo(ra_remover, sistema)
            elif op == "3":
                if not self.amigos:
                    print("Você não tem amigos para comparar.")
                    continue
                for ra in self.amigos:
                    amigo = sistema.buscar_usuario(ra)
                    if amigo:
                        comuns = set(self.materias_interesse) & set(amigo.materias_interesse)
                        print(f"\n📘 Matérias em comum com {amigo.nome} ({ra}):")
                        if comuns:
                            for m in comuns:
                                print(f" - {m}")
                        else:
                            print("Nenhuma matéria em comum.")
            elif op == "0":
                break
            else:
                print("Opção inválida.")
        print("-" * 40)

    def ver_notificacoes(self):
        print("\n🔔 NOTIFICAÇÕES:")
        if not self.notificacoes:
            print("Nenhuma notificação.")
        else:
            for i, n in enumerate(self.notificacoes, 1):
                print(f"{i}. {'✔' if n.lida else '❗'} {n.mensagem}")
                n.lida = True
        print("-" * 40)

class Sistema:
    def __init__(self):
        self.usuarios = self.carregar_usuarios()
        self.grupos = {}

    def carregar_usuarios(self):
        usuarios = []
        if not os.path.exists(ARQUIVO_CSV):
            return usuarios

        with open(ARQUIVO_CSV, "r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                usuarios.append(Perfil(
                    row["nome"],
                    row["ra"],
                    row["email"],
                    row["materias"].split(";") if row["materias"] else [],
                    row["amigos"].split(";") if row["amigos"] else [],
                    int(row["grupos"])
                ))
        return usuarios

    def buscar_usuario(self, ra):
        for u in self.usuarios:
            if u.ra == ra:
                return u
        return None

    def buscar_nome_por_ra(self, ra):
        usuario = self.buscar_usuario(ra)
        return usuario.nome if usuario else f"RA {ra} (não encontrado)"

    def adicionar_usuario_ao_grupo(self, usuario, materia):
        if materia not in self.grupos:
            self.grupos[materia] = Grupo(materia)
        self.grupos[materia].adicionar_membro(usuario)

def menu():
    sistema = Sistema()

    ra = input("Digite seu RA: ").strip()
    usuario = sistema.buscar_usuario(ra)

    if not usuario:
        nome = input("RA não encontrado. Digite seu nome: ")
        email = input("Digite seu email institucional: ")
        usuario = Perfil(nome, ra, email)
        sistema.usuarios.append(usuario)
        print("✅ Usuário criado com sucesso!")
    else:
        print(f"👋 Bem-vindo de volta, {usuario.nome}!")

    usuario.mostrar_dashboard(sistema)

    while True:
        print("\n📋 MENU")
        print("1. Alterar nome")
        print("2. Alterar email")
        print("3. Adicionar matéria de interesse")
        print("4. Ver amigos (gerenciar e comparar matérias)")
        print("5. Ver notificações")
        print("6. Ver dashboard")
        print("0. Sair")

        op = input("Escolha uma opção: ").strip()

        if op == "1":
            novo_nome = input("Novo nome: ")
            usuario.nome = novo_nome
        elif op == "2":
            novo_email = input("Novo email: ")
            usuario.email = novo_email
        elif op == "3":
            materia = input("Nome da matéria: ")
            usuario.adicionar_materia(materia, sistema)
        elif op == "4":
            usuario.ver_amigos(sistema)
        elif op == "5":
            usuario.ver_notificacoes()
        elif op == "6":
            usuario.mostrar_dashboard(sistema)
        elif op == "0":
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida.")

        usuario.salvar(sistema.usuarios)

if __name__ == "__main__":
    menu()
