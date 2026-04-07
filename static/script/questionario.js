 let secaoAtual = 0;
        const secoes = document.querySelectorAll('.secao');
        const totalSecoes = secoes.length;
        const btnProximo = document.getElementById('btnProximo');
        const btnAnterior = document.getElementById('btnAnterior');
        const divSubmit = document.getElementById('divSubmit');
        const progressFill = document.getElementById('progressFill');
        
        function atualizarProgresso() {
            const progresso = ((secaoAtual + 1) / totalSecoes) * 100;
            progressFill.style.width = progresso + '%';
        }
        
        function validarSecaoAtual() {
            const secao = secoes[secaoAtual];
            const camposObrigatorios = secao.querySelectorAll('[required]');
            let valido = true;
            
            camposObrigatorios.forEach(campo => {
                if (!campo.value || campo.value === '') {
                    campo.style.borderColor = 'red';
                    valido = false;
                } else {
                    campo.style.borderColor = '#e0e0e0';
                }
            });
            
            if (!valido) {
                alert('Por favor, preencha todos os campos obrigatórios antes de continuar!');
            }
            
            return valido;
        }
        
        function mudarSecao(direcao) {
            const novaSecao = secaoAtual + direcao;
            
            if (direcao === 1 && !validarSecaoAtual()) {
                return;
            }
            
            if (novaSecao >= 0 && novaSecao < totalSecoes) {
                secaoAtual = novaSecao;
                
                // Mostrar/esconder seções
                secoes.forEach((secao, index) => {
                    if (index === secaoAtual) {
                        secao.classList.add('active');
                    } else {
                        secao.classList.remove('active');
                    }
                });
                
                // Configurar botões
                if (secaoAtual === totalSecoes - 1) {
                    btnProximo.style.display = 'none';
                    divSubmit.style.display = 'flex';
                } else {
                    btnProximo.style.display = 'block';
                    divSubmit.style.display = 'none';
                }
                
                if (secaoAtual === 0) {
                    btnAnterior.style.display = 'none';
                } else {
                    btnAnterior.style.display = 'block';
                }
                
                atualizarProgresso();
            }
        }
        
        function adicionarCompetencia() {
            const input = document.getElementById('input_nova_comp');
            const nomeComp = input.value.trim();
            const lista = document.getElementById('lista-competencias');
            
            if (nomeComp === "") {
                alert("Digite o nome da competência!");
                return;
            }
            
            // Verificar se já existe na lista
            const checkboxes = lista.querySelectorAll('input[type="checkbox"]');
            let existe = false;
            checkboxes.forEach(cb => {
                const label = cb.nextElementSibling;
                if (label && label.textContent.toLowerCase() === nomeComp.toLowerCase()) {
                    existe = true;
                    cb.checked = true;
                }
            });
            
            if (existe) {
                alert("Esta competência já está na lista! Ela foi selecionada automaticamente.");
                input.value = "";
                return;
            }
            
            // Criar novo item
            const novoId = 'nova_' + Date.now();
            const novoItem = document.createElement('div');
            novoItem.className = 'competencia-item';
            novoItem.innerHTML = `
                <input type="checkbox" name="novas_competencias" value="${nomeComp.replace(/"/g, '&quot;')}" id="${novoId}" checked>
                <label for="${novoId}">${nomeComp} ✨</label>
            `;
            
            lista.appendChild(novoItem);
            input.value = "";
            input.focus();
            
            // Scroll para o novo item
            novoItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        // Permitir Enter para adicionar competência
        document.getElementById('input_nova_comp').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                adicionarCompetencia();
            }
        });
        
        // Inicializar
        atualizarProgresso();
        
        // Remover bordas vermelhas ao digitar
        document.querySelectorAll('input, select').forEach(campo => {
            campo.addEventListener('input', function() {
                this.style.borderColor = '#e0e0e0';
            });
        });