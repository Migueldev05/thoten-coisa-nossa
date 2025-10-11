// Executa o script quando o conteúdo HTML da página estiver totalmente carregado
document.addEventListener('DOMContentLoaded', function() {

    // --- LÓGICA PARA A PÁGINA DE CATÁLOGO (RF02) ---
    const botoesAdicionar = document.querySelectorAll('.btn-adicionar');
    if (botoesAdicionar.length > 0) {
        botoesAdicionar.forEach(button => {
            button.addEventListener('click', function() {
                const produto = {
                    nome: this.dataset.nome,
                    preco: parseFloat(this.dataset.preco),
                    imagem: this.dataset.imagem
                };

                fetch('/adicionar_ao_carrinho', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(produto),
                })
                .then(response => response.json())
                .then(data => {
                    // Se a resposta do servidor for bem-sucedida, mostra a mensagem
                    alert(data.mensagem);
                })
                .catch(error => {
                    // ATUALIZAÇÃO: Se houver um erro, agora mostra um alerta
                    console.error('Erro ao adicionar item:', error);
                    alert('Ocorreu um erro ao adicionar o item. Verifique o console do servidor.');
                });
            });
        });
    }

    // --- LÓGICA PARA A PÁGINA DO CARRINHO (RF03) ---

    // Botão de Limpar o Carrinho
    const botaoLimpar = document.getElementById('btn-limpar');
    if (botaoLimpar) {
        botaoLimpar.addEventListener('click', function() {
            if (confirm('Tem certeza que deseja esvaziar o carrinho?')) {
                fetch('/limpar_carrinho', { method: 'POST' })
                .then(() => {
                    window.location.reload();
                });
            }
        });
    }

    // Botões de Remover Item Individual
    const botoesRemover = document.querySelectorAll('.btn-remover');
    if (botoesRemover.length > 0) {
        botoesRemover.forEach(button => {
            button.addEventListener('click', function() {
                const nomeProduto = this.dataset.nome;
                if (confirm(`Tem certeza que deseja remover ${nomeProduto}?`)) {
                    fetch('/remover_item', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nome: nomeProduto }),
                    })
                    .then(() => {
                        window.location.reload();
                    });
                }
            });
        });
    }
});