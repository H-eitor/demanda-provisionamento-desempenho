# Atividade 2 - Demanda, Provisionamento e Desempenho

## Instruções

Essa é a segunda atividade avaliativa da disciplina e vocês devem desenvolver (em grupos de três) . Essas aplicações vão servir de base para estudar a relação entre demanda, desempenho, utilização de recursos e provisionamento.

Após o desenvolvimento, vocês deverão configurar uma máquina virtual (VirtualBox), fazer o deploy das aplicações desenvolvidas e realizar experimentos com diferentes níveis de demanda e configurações de recursos computacionais.

O objetivo é demonstrar experimentalmente como a variação da demanda afeta o desempenho e a utilização dos recursos, e como o provisionamento de recursos computacionais pode influenciar o comportamento da aplicação.

Para tal, vocês devem criar um repositório na organização da disciplina, que vai armazenar todos os artefatos de software gerados (código, scripts, textos, resultados dos experimentos etc.).

Especificamente, vocês devem fazer o seguinte:

- Desenvolver três aplicações web (apenas backend), com diferentes perfis computacionais (CPU-bound, Memory-bound ou IO-bound), usando uma linguagem de programação de sua preferência;

- Manter o código atualizado no repositório criado;

- Executar e testar o funcionamento das aplicações em uma máquina local;

- Configurar uma máquina virtual (VirtualBox) seguindo o roteiro disponibilizado e fazer o deploy de uma das aplicações desenvolvidas;

- Executar e testar o funcionamento da aplicação selecionada na máquina virtual (vocês devem me mostrar isso em sala);

- Realizar experimentos na máquina virtual, variando a demanda e a configuração dos recursos computacionais. Utilizem pelo menos quatro cenários de provisionamento e diferentes níveis de demanda para cada cenário;

- Coletar dados de desempenho e utilização de recursos durante os testes, incluindo métricas como tempo de resposta, vazão (requisições por segundo), utilização de CPU e consumo de memória, conforme aplicável;

- Demonstrar, por meio de gráficos e da interpretação dos resultados, a relação entre demanda, provisionamento, desempenho e utilização de recursos. Identifiquem situações em que o aumento da demanda provoca degradação do desempenho e discutam como a alteração dos recursos provisionados afeta esse comportamento;

- Produzir um documento descrevendo os experimentos realizados, a metodologia, os resultados obtidos e as conclusões, seguindo o template disponibilizado;

- Responder ao formulário abaixo com as informações de entrega da atividade (cada integrante do grupo deve responder uma vez).

- Vocês devem me mostrar as aplicações executando no LCC.

- O disco VDI pode ser encontrado no link abaixo (nos LCCs, usem a versão em /local/uasc).

- Roteiro para configuração da máquina virtual e deploy da aplicação

- Template do documento com os resultados da atividade

## Arquivos

- [Atividade a ser entregue](docs/att.md)

- [Roteiro da aplicação](docs/roteiro.md)

## Execução

| Endpoint  | Perfil       | Parâmetro | Default   | Limite         | Recurso mais afetado |
| --------- | ------------ | --------- | --------- | -------------- | -------------------- |
| `/`       | health check | -         | -         | -              | -                    |
| `/cpu`    | CPU-bound    | `n`       | 3.000.000 | 1 a 50.000.000 | CPU                  |
| `/memory` | Memory-bound | `size`    | 1500      | 1 a 5000       | RAM                  |
| `/io`     | I/O-bound    | `size`    | 20        | 1 a 500        | Disco                |

### Servidor

```
uvicorn server:app --host 0.0.0.0 --port 8000 --workers <nº de vCPUs>
```

### CPU-bound

`n` iterações acumulando `i * i`

Exemplo:
```
curl "http://localhost:8000/cpu?n=3000000"
```

### Memory-bound

Soma todos os elementos de uma matriz `size x size`

Exemplo:
```
curl "http://localhost:8000/memory?size=1500"
```

### IO-bound

Repete `size` ciclos de escrita de 1 MB em um arquivo temporário. O volume escrito em disco é `size` MB e o volume lido também

Exemplo:
```
curl "http://localhost:8000/io?size=20"
```