# Sistema de Grupos de Estudo

##  Visão Geral

Este projeto implementa um sistema completo para gerenciamento de grupos de estudo, desenvolvido como trabalho para a disciplina de Engenharia de Software. O sistema é composto por quatro módulos independentes, cada um implementando um padrão de projeto específico e focando em diferentes aspectos da gestão de grupos de estudo.

##  Tecnologias Utilizadas

- **Linguagem**: Python
- **Tipo de arquivo**: CSV (para armazenamento de dados)
- **Arquitetura**: MVC (Model-View-Controller)

##  Módulos e Padrões de Projeto

### 1. Configurações e Dashboard Pessoal (Caio)
- **Padrão de Projeto**: Singleton
- **Funcionalidades**:
  - Gerenciamento de perfil de usuário
  - Dashboard personalizado
  - Configurações de conta
  - Gerenciamento de matérias de interesse

### 2. Criação de Grupos com Chat (Matheus)
- **Padrão de Projeto**: Factory Method
- **Funcionalidades**:
  - Criação de diferentes tipos de usuários (padrão, moderador, administrador)
  - Sistema de chat para grupos
  - Gerenciamento de permissões

### 3. Criação Automática de Grupos (Vitor)
- **Padrão de Projeto**: Observer
- **Funcionalidades**:
  - Formação automática de grupos baseada em similaridades
  - Notificações de eventos do sistema
  - Algoritmo de matching para agrupar estudantes compatíveis

### 4. Fórum de Perguntas e Respostas (João)
- **Padrão de Projeto**: Command Pattern
- **Funcionalidades**:
  - Sistema de perguntas e respostas
  - Registro de interações
  - Consulta de histórico

## 📥 Como Baixar

Para obter o código-fonte do projeto, execute o seguinte comando:

```bash
git clone https://github.com/MatheusOtenio/Trabalho-2-Engenharia-Software.git
```

Ou baixe diretamente do GitHub acessando [este link](https://github.com/MatheusOtenio/Trabalho-2-Engenharia-Software.git).

##  Como Executar

### Pré-requisitos
- Python 3.6 ou superior
- Pandas (para o módulo de criação automática de grupos)

### Instalação de Dependências

```bash
pip install pandas
```

### Executando o Programa

1. Navegue até o diretório do projeto:
   ```bash
   cd Trabalho-2-Engenharia-Software
   ```

2. Execute o programa principal:
   ```bash
   python main.py
   ```

3. No menu principal, selecione o módulo que deseja utilizar:
   - Opção 1: Projeto do Caio (Gerenciamento de Perfis e Grupos)
   - Opção 2: Projeto do João (Sistema de Grupos)
   - Opção 3: Projeto do Matheus (Chat de Grupos de Estudo)
   - Opção 4: Projeto do Viana (Montagem de Grupos)

##  Estrutura do Projeto

```
trab2-eng-soft/
├── main.py                  # Ponto de entrada principal
├── caio/                    # Módulo de Configurações e Dashboard (Singleton)
│   ├── main.py
│   ├── sistema_controller.py
│   ├── perfil.py
│   └── ...
├── matheus/                 # Módulo de Criação de Grupos com Chat (Factory Method)
│   ├── main.py
│   ├── user_factory.py
│   ├── controller.py
│   └── ...
├── viana/                   # Módulo de Criação Automática de Grupos (Observer)
│   ├── main.py
│   ├── modelCriarGrupo.py
│   ├── controllerCriarGrupo.py
│   └── ...
└── jao/                     # Módulo de Fórum de Perguntas e Respostas (Command Pattern)
    ├── main.py
    ├── controller.py
    ├── model.py
    └── ...
```

##  Contribuidores

- **Caio**: Configurações e Dashboard Pessoal (Padrão Singleton)
- **Matheus**: Criação de Grupos com Chat (Padrão Factory Method)
- **Vitor**: Criação Automática de Grupos (Padrão Observer)
- **João**: Fórum de Perguntas e Respostas (Padrão Command Pattern)
