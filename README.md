# Sistema de Biblioteca

Um sistema moderno e intuitivo para gerenciamento de biblioteca, desenvolvido em Python usando o framework Flet para interface gráfica.

## 📋 Características

- Interface gráfica moderna e responsiva
- Sistema de login com diferentes níveis de acesso (admin/usuário)
- Gerenciamento completo de livros (CRUD)
- Upload e visualização de capas de livros
- Sistema de avaliação de livros
- Controle de quantidade de livros
- Interface drag-and-drop para imagens
- Banco de dados SQLite para persistência de dados

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Flet (Framework de UI)
- SQLite3 (Banco de Dados)
- Bibliotecas Python:
  - os
  - shutil
  - tempfile
  - datetime

## 💻 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-biblioteca.git
cd sistema-biblioteca
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

1. Execute o sistema:
```bash
python sistema_lib.py
```

2. Faça login com as credenciais padrão do administrador:
   - Email: admin@admin.com
   - Senha: admin123

3. No painel administrativo você pode:
   - Abra a tela cheia para navegação completa
   - Visualizar e editar informações do usuário
   - Gerenciar livros
   - Gerenciar imagens
   - Adicionar novos livros
   - Editar livros existentes
   - Excluir livros
   - Visualizar todos os livros cadastrados

## 📁 Estrutura do Projeto

- `sistema_lib.py`: Arquivo principal do sistema
- `db.py`: Gerenciamento do banco de dados
- `tela_inicial.py`: Tela de login
- `tela_admin.py`: Painel administrativo
- `tela_livros.py`: Visualização de livros
- `adicionar_livro.py`: Interface para adicionar livros
- `editar_excluir_livro.py`: Interface para editar/excluir livros
- `editor_usuarios.py`: Interface para editar usuários
- `img/`: Diretório para imagens de capas de livros
- `editar_excluir_usuarios.py`: Interface para editar/excluir usuários

## 🔧 Funcionalidades Detalhadas

### Gerenciamento de Usuários
- Cadastro completo com:
  - Nome
  - Email
  - Senha
  - Tipo (admin/usuário)
  - CPF
  - Data de criação
- Edição de informações:
  - Atualização de dados pessoais
  - Alteração de senha
  - Modificação de permissões
- Controle de empréstimos:
  - Número de livros emprestados
  - Histórico de empréstimos
  - Limite de empréstimos
- Interface intuitiva para administradores:
  - Lista de todos os usuários
  - Filtros de busca
  - Ações em lote

### Sistema de Arquivos
- Diretório `img/`:
  - Armazenamento organizado de capas
  - Nomenclatura padronizada
  - Backup automático
  - Limpeza de arquivos não utilizados
- Processamento de imagens:
  - Redimensionamento automático
  - Otimização de qualidade
  - Validação de formatos
- Segurança:
  - Verificação de extensões
  - Limite de tamanho
  - Proteção contra uploads maliciosos

### Sistema de Login
- Autenticação de usuários
- Diferentes níveis de acesso (admin/usuário)
- Sessão persistente

### Gerenciamento de Livros
- Cadastro com:
  - Título
  - Avaliação (0-10)
  - Quantidade em estoque
  - Capa do livro (suporta drag-and-drop)
- Edição completa de informações
- Exclusão com confirmação
- Visualização em lista

### Gerenciamento de Imagens
- Upload de capas
- Suporte a formatos: PNG, JPG, JPEG
- Armazenamento otimizado
- Preview em tempo real

### Banco de Dados
- Tabelas:
  - usuarios (id, nome, email, senha, tipo, cpf, etc.)
  - livros (id, nome_livro, nota, quantidade, imagem_path)
- Backup automático
- Índices otimizados

## 🔒 Segurança

- Senhas armazenadas com segurança
- Validação de inputs
- Tratamento de erros
- Confirmação para ações críticas

## 🎨 Interface

- Design moderno e intuitivo
- Cores consistentes
- Feedback visual para ações
- Mensagens de erro claras
- Navegação simplificada

## ⚙️ Configurações

O sistema cria automaticamente:
- Banco de dados (usuarios.db)
- Diretório para imagens
- Usuário administrador padrão

## 📝 Logs e Feedback

O sistema fornece feedback visual para:
- Sucesso nas operações
- Erros de validação
- Confirmações de ações
- Status das operações

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo (LICENSE) para mais detalhes.

## ✨ Próximas Atualizações

- [ ] Sistema de empréstimo de livros
- [ ] Sistema de compra de livros
- [ ] Adição de tela de relatórios
- [ ] Adição de tela de para tipo do usuário "usuario" e "coordenador" 
- [ ] Relatórios e estatísticas
- [ ] Interface web
- [ ] Backup na nuvem
- [ ] Sistema de notificações
- [ ] Integração com APIs externas

## 🐛 Bugs Conhecidos

- Nenhum bug conhecido até o momento

## 📞 Suporte

Para suporte, envie um email para klebersonksp10@gmail.com

## 🙋‍♂️ Autores

- Kleberson Santana Pinto- [GitHub](https://github.com/KK47Force)

---

Desenvolvido com ❤️ por Kleberson Santana Pinto
