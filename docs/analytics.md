# Analytics, Search Console e prévia de links

[← voltar ao README](../README.md)

## Sumário

1. [Visão geral](#visão-geral)
2. [Eventos enviados ao GA4](#eventos-enviados-ao-ga4)
3. [Configuração feita no GA4](#configuração-feita-no-ga4)
4. [Consentimento de cookies](#consentimento-de-cookies)
5. [Tráfego interno](#tráfego-interno)
6. [Google Search Console](#google-search-console)
7. [Prévia de links](#prévia-de-links-whatsapp-facebook-instagram)
8. [Como validar](#como-validar)
9. [Conexão pela API (Claude Code e scripts)](#conexão-pela-api-claude-code-e-scripts)
10. [Relatórios](#relatórios)
11. [Validação completa](#validação-completa)
12. [Vantagens do que foi feito](#vantagens-do-que-foi-feito)
13. [Pendências](#pendências)
14. [Possíveis próximos passos](#possíveis-próximos-passos)

---

## Visão geral

| Item | Valor |
|---|---|
| Conta GA | Remessa Japao |
| Propriedade GA4 | Calculadora remessa (fuso: Japão), ID `561947228` |
| Fluxo da Web | Site Github Pages, `https://andreyoshimura.github.io/remessa-japao` |
| ID de medição | `G-HRC1WBVL2V` |
| Medição otimizada | Ativada (visualizações, rolagem, cliques de saída etc.) |
| Search Console | Propriedade por prefixo de URL, verificada por meta tag e vinculada ao GA |

O GA4 é carregado pelo próprio `index.html`, e não pelo snippet padrão do Google, para respeitar o aviso de cookies.

## Eventos enviados ao GA4

| Evento | Quando dispara | Parâmetros |
|---|---|---|
| `page_view` | Abertura da página (automático) | `ref`, `origem` (`pagina`/`embed`) |
| `conversao` | 1,5 s depois de a pessoa parar de digitar, **sempre que o valor, a direção ou a cotação mudar**. Só depois que a pessoa mexe em algo: o valor que já vem na página não conta. | pacote da conversão (abaixo) |
| `chip_valor` | Clique num valor rápido (¥50 mil, R$ 500…) | pacote da conversão |
| `inverter` | Clique no botão ⇅ | pacote da conversão |
| `outra_cotacao` | Abriu "Usar outra cotação" | pacote da conversão |
| `compartilhar_whatsapp` | Clique em "Mandar esta conversão no WhatsApp" (conversor) ou "Mandar este checklist no WhatsApp" (`visto.html`) | conversor: pacote da conversão; visto: `origem: "visto"` e `visto` (só o link vai na mensagem, com `?ref=whatsapp`; as respostas não) |
| `clique_rede_social` | Clique num ícone do rodapé | pacote da conversão + `rede` (`instagram`/`facebook`/`tiktok`/…) |
| `clique_afiliado` | Clique no botão da Wise (quando ligado) | pacote da conversão |
| `checklist_visto` | `visto.html`: escolheu o tipo de visto | `visto` (`permanente`/`teijusha`/`conjuge`/`outro`) |
| `checklist_resultado` | `visto.html`: clicou em "Ver meu resultado" | `visto`, `em_dia`, `conferir`, `resolver` (só contagens; as respostas não são enviadas) |
| `clique_rede_social` (visto) | `visto.html`: ícones "Siga o Radar Nihon" no resultado | `rede`, `origem: "visto"` |
| (config) `parceiro` | `?p=<código>` no conversor ou na `visto.html`: versão de parceiro | enviado no `gtag("config")` junto com `ref` (padrão: o `ref` do parceiro) |
| `enviar_resultado` | `visto.html`: "Mandar minha lista no WhatsApp" ou "Cartão do resultado" | `formato` (`lista`/`cartao`), `visto`. A lista e o cartão são montados no celular; o GA não recebe o conteúdo. Links com `?ref=lista` e `?ref=cartao` |

**Pacote da conversão:** `direcao`, `faixa_ienes`, `valor_ienes`, `valor_reais`, `cotacao`, `cotacao_fonte` e `ref`. Ele vai em todos os eventos acima desde 2026-11-04 no fuso do GA (Tóquio), que corresponde a 03/11 à noite no Brasil.
| `cookies_aceitos` / `cookies_recusados` | Resposta ao aviso de cookies | — |
| `cotacao_erro` | AwesomeAPI e PTAX falharam | — |

**Valores dos parâmetros:**
- `direcao`: `iene_para_real` ou `real_para_iene`.
- `faixa_ienes`: sempre calculada em ienes, nas duas direções. Valores possíveis: `ate_50mil`, `50_100mil`, `100_200mil`, `200_300mil`, `300mil_mais`.
- `valor_ienes`: número inteiro, o valor da conversão em ienes (o digitado, ou o equivalente quando a pessoa digitou em reais).
- `valor_reais`: número com 2 casas, o valor da conversão em reais (o digitado, ou o equivalente quando a pessoa digitou em ienes).
- `cotacao`: reais por ¥1 usados naquela conversão (ex.: `0.03444`). Permite reconstruir a conversão no futuro, quando o câmbio for outro.
- `cotacao_fonte`: `awesomeapi`, `ptax` (reserva do Banco Central) ou `manual` (a pessoa digitou a própria cotação).
- `ref`: origem, `github-pages` por padrão, ou o valor de `?ref=`.

**Dados anteriores a 2026-11-04 (fuso do GA):**
- Toda visita gerava uma `conversao` de ¥100.000 sozinha, pelo valor que vem preenchido. Por isso há excesso de ¥100.000 nesse período.
- Conversões repetidas na mesma faixa não eram registradas.
- Não havia `valor_reais` nem `cotacao`.

Para analisar valores, use dados a partir de **2026-11-04**. O `scripts/ga-relatorio.py` já separa os dois períodos.

**Atribuição do WhatsApp:** o link compartilhado leva `utm_source=whatsapp&utm_medium=compartilhamento`. Em **Aquisição → Aquisição de tráfego** essas visitas aparecem como `whatsapp / compartilhamento`.

## Configuração feita no GA4

Feita à mão em 2026-11-02. Os eventos principais foram criados pela Admin API em 2026-11-03. Para ver o estado atual: `scripts/ga-status.sh`.

| Onde | O quê | Situação |
|---|---|---|
| Exibição de dados → Definições personalizadas | Dimensão **Direção** → `direcao` (Evento) | ✅ |
| 〃 | Dimensão **Faixa de ienes** → `faixa_ienes` (Evento) | ✅ |
| 〃 | Dimensão **Origem** → `ref` (Evento) | ✅ |
| 〃 | Dimensão **Rede Social** → `rede` (Evento) | ✅ |
| 〃 | Dimensão **Fonte da cotação** → `cotacao_fonte` (Evento) | ✅ criada pela Admin API em 2026-11-03 |
| 〃 | Métrica **Valor em reais** → `valor_reais` (Evento, Padrão) | ✅ criada pela Admin API em 2026-11-03. Como "Padrão" e não "Moeda": o GA exige que métrica de moeda seja marcada como receita ou custo, e o valor convertido não é nenhum dos dois. |
| 〃 | Métrica **Cotação usada** → `cotacao` (Evento, Padrão) | ✅ criada pela Admin API em 2026-11-03 |
| 〃 | Métrica **Valor em ienes** → `valor_ienes` (Evento, Padrão) | ✅ criada (2026-11-02). A dimensão "Valor ienes" criada por engano foi arquivada, confirmado pela API em 2026-11-03. |
| Coleta e modificação de dados → Filtros de dados | **Internal Traffic**: excluir `traffic_type = internal`, estado **Ativo** | ✅ |
| Vínculos de produtos → Links do Search Console | Vínculo com `https://andreyoshimura.github.io/remessa-japao/` e o fluxo Site Github Pages | ✅ |
| Exibição de dados → Eventos | ⭐ evento principal em `compartilhar_whatsapp` e `clique_rede_social` (uma vez por evento) | ✅ criados pela Admin API em 2026-11-03 (`scripts/ga-eventos-principais.sh`) |
| Coleta e modificação de dados → Retenção de dados | Eventos: **14 meses** (padrão é 2) | ✅ (2026-11-02) |
| Coleta e modificação de dados → Coleta de dados | **Google Signals desligado**: evita limites que escondem dados num site pequeno, e o site nega consentimento de anúncios de qualquer jeito | ✅ desligado pelo painel; confirmado pela API em 2026-11-03 (`scripts/ga-google-signals.sh`) |

Os eventos principais `close_convert_lead` e `qualify_lead`, criados automaticamente pelo objetivo "Gerar leads", já foram removidos. Hoje os eventos principais são `compartilhar_whatsapp`, `clique_rede_social` e `purchase` (padrão do GA, o site não envia).

Os eventos `calculo` e `abrir_ajustes` que aparecem nos relatórios vêm da primeira versão do site (calculadora de remessa) e não são mais enviados.

## Consentimento de cookies

Implementado com **Consent Mode v2**:

```
padrão:   ad_storage, ad_user_data, ad_personalization = denied
          analytics_storage = denied   (ou granted, se já aceitou antes)
aceitar → analytics_storage = granted  + evento cookies_aceitos
recusar → analytics_storage = denied   + evento cookies_recusados
```

- A escolha fica no `localStorage` (`ccj_consent`).
- **Sem aceite:** o GA recebe só sinais sem cookies e estima os números (modelagem).
- **No modo embutido** o aviso não aparece e a visita fica sem cookies.
- **"Preferências de cookies"** no rodapé reabre o aviso.

## Tráfego interno

Serve para as suas próprias visitas não contarem nos relatórios.

1. Abra uma vez **https://andreyoshimura.github.io/remessa-japao/?interno=1** em cada navegador ou celular que você usa. Isso grava `ccj_interno=1` no navegador.
2. A partir daí, o site envia `traffic_type=internal`, e o filtro **Internal Traffic** (ativo) descarta essas visitas.
3. Para **testar algo no GA**, abra com `?interno=0`, teste e depois volte com `?interno=1`.

O filtro descarta os dados **de vez**. Visitas internas não podem ser recuperadas depois.

**Atenção (análise de 2026-11-04):** 6 das 10 pessoas da primeira semana vieram da cidade de quem testa, em aparelhos
ainda sem `?interno=1`. Abra o link em **todo** celular e navegador seu e de quem testa com você. Para ler os
números sem essa cidade, use `GA_EXCLUIR_CIDADES` no relatório (veja [Relatórios](#relatórios)); o nome da cidade
fica só no seu ambiente, nunca no repositório.

**Robôs (desde 2026-11-04):** navegadores automatizados (`navigator.webdriver`) e agentes como `HeadlessChrome`,
`bot`, `crawler`, `spider`, `Lighthouse`, `PageSpeed` e `facebookexternalhit` não carregam o GA. Eles apareciam
como visitas falsas dos EUA (Chrome no Linux, em inglês, num data center).

## Google Search Console

- **Propriedade:** prefixo de URL `https://andreyoshimura.github.io/remessa-japao/`. O tipo "Domínio" não funciona para `github.io`.
- **Verificação:** meta tag no `<head>` do `index.html`:
  ```html
  <meta name="google-site-verification" content="BanQ_ppxaXERI9g8SKpXYfudEKwdMDiMg2NF3ZrcAw0" />
  ```
  **Não remover.** O Google confere de tempos em tempos.
- **Vínculo com o GA:** feito. Os dados aparecem em **Relatórios → Aquisição → Search Console** depois que o site começar a aparecer no Google.
- **Acesso pela API (2026-11-04):** `scripts/sc-relatorio.py` lê as buscas que mostram o site (consultas, países,
  aparelho, dia), com filtro por país (`jpn` = Japão). Usa o mesmo ADC, com o escopo `webmasters` (completo desde 2026-11-05, para enviar o sitemap pela API). O vínculo
  com o GA mostra esses dados só no painel; a API do GA não os entrega.
- **Indexação:** a Inspeção de URL mostrou "O URL está no Google" em 2026-11-03. O Google indexou sozinho, sem precisar de "Solicitar indexação". Se o site mudar muito, dá para pedir de novo em **Inspeção de URL → Solicitar indexação**.

## Prévia de links (WhatsApp, Facebook, Instagram)

Tags Open Graph no `<head>`:

| Tag | Valor |
|---|---|
| `og:title` | Conversor iene ⇄ real |
| `og:description` | Quanto valem seus ienes em reais hoje? Cotação do dia, sem cadastro. |
| `og:image` | `https://andreyoshimura.github.io/remessa-japao/og.png` (1200×630, PNG, ~33 KB) |
| `og:url` / canonical | `https://andreyoshimura.github.io/remessa-japao/` |
| `og:site_name` | Radar Nihon |
| `twitter:card` | `summary_large_image` |

**Cuidados:**
- **Use `⇄` e não `↔` nos títulos.** O Facebook transforma `↔` em emoji e mostra um quadradinho.
- **Mantenha a imagem abaixo de ~300 KB.** O WhatsApp ignora imagens grandes.
- **Cache:** WhatsApp e Facebook guardam a prévia por URL.
  - **Mensagens já enviadas** mantêm a prévia antiga para sempre.
  - **Botão do site:** o link leva `&v=4`. Ao mudar título, descrição ou imagem, aumente esse número no código.
  - **Link colado à mão:** adicione `?v=N` para forçar a prévia nova.
  - **Facebook e Instagram:** https://developers.facebook.com/tools/debug/ → **Extrair novamente**. O aviso "fb:app_id ausente" pode ser ignorado.

## Como validar

### 1. Eventos em tempo real
1. Abra `https://andreyoshimura.github.io/remessa-japao/?interno=0` numa aba anônima, sem bloqueador de anúncios.
2. Clique em **Aceitar**, depois em **¥200 mil**, espere 2 s, clique em **⇅**, em **Mandar no WhatsApp** (pode fechar) e no **Instagram**.
3. No GA, abra **Relatórios → Tempo real**. Devem aparecer `page_view`, `cookies_aceitos`, `chip_valor`, `conversao`, `inverter`, `compartilhar_whatsapp` e `clique_rede_social`. Clique num evento para ver os parâmetros.
4. Volte a marcar o navegador com `?interno=1`.

### 2. No navegador, sem depender do GA
Aperte F12, abra **Rede**, filtre por `collect`. Cada clique gera uma requisição `…/g/collect?v=2…`. No **Payload**, o campo `en` é o nome do evento.

### 3. Search Console
- **Configurações → Verificação de propriedade:** deve estar "proprietário verificado".
- **Inspeção de URL → Testar URL publicado:** deve dizer "O URL está disponível para o Google".

### 4. Depois de 24 a 48 horas
- **Relatórios → Engajamento → Eventos:** os eventos aparecem com contagens.
- **Aquisição → Aquisição de tráfego:** aparece `whatsapp / compartilhamento`.
- **Search Console → Desempenho:** as primeiras buscas, em dias ou semanas.

### 5. Prévia de links
No Depurador do Facebook, depois de "Extrair novamente", devem aparecer a imagem azul e o título "Conversor iene ⇄ real", sem o quadradinho.

## Conexão pela API (Claude Code e scripts)

Serve para ler relatórios sem abrir o painel (pelo MCP oficial) e para automatizar a administração (pelos scripts da Admin API). Configurada em 2026-11-03.

### Como funciona

| Peça | O que é |
|---|---|
| Projeto do Google Cloud | `radar-nihon-analytics`, dedicado, dentro da organização do Workspace. APIs ativas: Google Analytics Data API, Google Analytics Admin API, Cloud Resource Manager API (necessária para o projeto de cota) e **Search Console API** (desde 2026-11-04). |
| Autenticação | **ADC (Application Default Credentials) com cliente OAuth próprio**, do tipo "App para computador", com tela de consentimento **Interna**. |
| Escopos | `analytics.readonly` (relatórios), `analytics.edit` (administração), `cloud-platform` (projeto de cota), `webmasters` (buscas e envio de sitemap no Search Console; leitura desde 2026-11-04, completo desde 2026-11-05). |
| MCP | [`analytics-mcp`](https://github.com/googleanalytics/google-analytics-mcp), oficial do Google, instalado com `pipx`. Só leitura. |
| Scripts | `scripts/*.sh`, chamam a Admin API com o token do ADC. |

**Por que ADC e não conta de serviço com chave JSON:**
- **Sem senha permanente:** a credencial é um token da sua conta, revogável em myaccount.google.com → Segurança.
- **Sem bloqueio de política:** a organização bloqueia criação de chaves de conta de serviço por padrão.
- **Sem usuário extra no GA:** o ADC usa as permissões que você já tem.
- **É o caminho do MCP oficial:** é o que a documentação dele recomenda.

Conta de serviço só valeria para automação sem ninguém por perto (CI ou servidor).

### Onde fica cada coisa (nada disso vai para o Git)

```
~/.local/opt/google-cloud-sdk/          gcloud (tarball oficial, sem install.sh)
~/.local/bin/gcloud-rn                  atalho: gcloud com CLOUDSDK_CONFIG isolado
~/.local/bin/radar-nihon-adc-login      atalho: login ADC com o cliente próprio
~/.local/bin/analytics-mcp              MCP oficial (pipx)
~/.config/radar-nihon/                  chmod 700
├── oauth-client.json                   cliente OAuth (chmod 600)
└── gcloud/                             configuração isolada do gcloud
    └── application_default_credentials.json   credencial ADC (chmod 600)
```

O `.bashrc` e o `.profile` não foram alterados. O `~/.local/bin` já faz parte do PATH.

### Passo a passo (para refazer em outra máquina)

1. **Instalar o gcloud** só extraindo o tarball oficial:
   ```bash
   mkdir -p ~/.local/opt
   curl -fsSLO https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
   tar -xzf google-cloud-cli-linux-x86_64.tar.gz -C ~/.local/opt
   ```
2. **Criar o atalho `~/.local/bin/gcloud-rn`** (chmod 755):
   ```sh
   #!/bin/sh
   export CLOUDSDK_CONFIG="$HOME/.config/radar-nihon/gcloud"
   exec "$HOME/.local/opt/google-cloud-sdk/bin/gcloud" "$@"
   ```
   E a pasta privada: `mkdir -p ~/.config/radar-nihon/gcloud && chmod 700 ~/.config/radar-nihon ~/.config/radar-nihon/gcloud`
3. **Login no gcloud:** `gcloud-rn auth login SEU_EMAIL`
4. **Projeto e APIs** (só na primeira vez; em outra máquina, pule):
   ```bash
   gcloud-rn projects create radar-nihon-analytics --organization=ID_DA_ORGANIZACAO
   gcloud-rn services enable analyticsdata.googleapis.com analyticsadmin.googleapis.com \
     cloudresourcemanager.googleapis.com searchconsole.googleapis.com --project=radar-nihon-analytics
   ```
5. **Cliente OAuth** (só na primeira vez), em https://console.cloud.google.com/auth/overview?project=radar-nihon-analytics:
   - Primeiros passos → público-alvo **Interno**.
   - Clientes → Criar cliente → **App para computador** → baixar o JSON.
   - Guardar: `mv ~/Downloads/client_secret_*.json ~/.config/radar-nihon/oauth-client.json && chmod 600 ~/.config/radar-nihon/oauth-client.json`
   - **Nunca colar esse JSON em chat nem no repositório.**
6. **Login ADC**, com o atalho `radar-nihon-adc-login`. Ele roda:
   ```sh
   gcloud-rn auth application-default login \
     --client-id-file="$HOME/.config/radar-nihon/oauth-client.json" \
     --scopes="https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics.edit,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/webmasters"
   chmod 600 "$HOME/.config/radar-nihon/gcloud/application_default_credentials.json"
   gcloud-rn auth application-default set-quota-project radar-nihon-analytics
   ```
   Na tela do Google deve aparecer o nome **"Radar Nihon Analytics (local)"**.
7. **MCP:**
   ```bash
   python3 -m pip install --user pipx
   ~/.local/bin/pipx install analytics-mcp
   ```
   O `.mcp.json` do repositório já aponta para `${HOME}/.local/bin/analytics-mcp` e para a credencial via `${HOME}`, sem nome de usuário no arquivo. Ao abrir o Claude Code nesta pasta, aprove o servidor `analytics-mcp`.

### Scripts

Os scripts que alteram algo rodam em **modo simulação** por padrão e só mudam com `--aplicar`. Todos podem ser rodados de novo sem efeito colateral.

| Script | O que faz |
|---|---|
| `scripts/ga-status.sh` | Só leitura: eventos principais, Google Signals, retenção, definições personalizadas e eventos dos últimos 28 dias. |
| `scripts/ga-definicoes.sh [--aplicar]` | Cria as dimensões e métricas personalizadas que faltarem (lista no próprio script). Ao criar um parâmetro novo no site, acrescente-o lá e rode. |
| `scripts/ga-eventos-principais.sh [--aplicar]` | Marca `compartilhar_whatsapp` e `clique_rede_social` como eventos principais (uma vez por evento). |
| `scripts/ga-google-signals.sh [--aplicar]` | Desliga o Google Signals, se estiver ligado (Admin API v1alpha). |
| `scripts/ga-relatorio.py [início] [fim]` | Só leitura (Data API): relatório completo em Markdown. Veja [Relatórios](#relatórios). |
| `scripts/sc-relatorio.py [país] [início]` | Só leitura (Search Console API): consultas, países, aparelho e dia. `jpn` filtra o Japão. |

Variáveis opcionais: `GA_PROPERTY` (padrão `561947228`), `GA_QUOTA_PROJECT`, `CLOUDSDK_CONFIG` e `GCLOUD`.

**Limites da API:**
- **Filtros de dados** (tráfego interno) não existem na Admin API, só no painel.
- **Search Console:** as buscas vêm pela Search Console API (`sc-relatorio.py`); indexação e verificação continuam só no painel.

### Segurança

- **Repositório público:** credencial, token e cliente OAuth ficam só em `~/.config/radar-nihon/`. O `.gitignore` bloqueia `*.json` (exceto `.mcp.json`), `client_secret*`, `*credentials*`, `*service-account*`, chaves (`*.pem`, `*.p12`, `*.key`) e `.env*`.
- **Revogar o acesso:** myaccount.google.com → Segurança → Apps de terceiros → "Radar Nihon Analytics (local)". Também dá para usar `gcloud-rn auth application-default revoke`.
- **Login expirado ou revogado:** rode `radar-nihon-adc-login` de novo.

## Relatórios

```bash
python3 -I scripts/ga-relatorio.py                    # desde o lançamento
python3 -I scripts/ga-relatorio.py 7daysAgo           # últimos 7 dias
python3 -I scripts/ga-relatorio.py 2026-11-04 today   # só com a captura nova do valor
GA_EXCLUIR_CIDADES="Cidade A" python3 -I scripts/ga-relatorio.py   # também sem a(s) cidade(s) dos testadores
python3 -I scripts/sc-relatorio.py jpn                # buscas no Google vindas do Japão (28 dias)
```

**Seções do relatório:**
- **Visão geral:** pessoas, pessoas novas, visitas, páginas, engajamento, tempo médio, eventos e eventos principais.
- **Por dia** e **de onde vieram** (origem / mídia).
- **Aparelho**, **país** e **cidade**.
- **Japão (métrica principal):** pessoas, visitas, engajamento e eventos principais só do Japão; com visitas, também origem, cidades e ações.
- **Sem as cidades de `GA_EXCLUIR_CIDADES`** (opcional).
- **Cliques e ações:** todos os eventos, com vezes e pessoas, e as **redes sociais clicadas**.
- **Valor convertido:**
  - total e média em ienes, total em reais, por direção;
  - um bloco separado só com a captura nova;
  - **faixas de valor**;
  - **valores dos botões rápidos**;
  - **valor no momento do compartilhamento** no WhatsApp;
  - **fonte e média da cotação**.

Os números **não ficam no repositório**, porque ele é público. O script gera o relatório na hora. Pelo MCP (`analytics-mcp`), dá para pedir os mesmos dados em linguagem natural no Claude Code.

**Como ler os números:**
- Datas no fuso da propriedade (**Ásia/Tóquio**). O tráfego interno já vem excluído.
- **Os números são um piso.** Quem recusa ou ignora o aviso de cookies envia ao GA só sinais anônimos (`gcs=G100`). Essas visitas **não aparecem no tempo real nem como pessoas** nos relatórios; servem apenas para estimativas, e só com volume grande. Navegadores com bloqueio (janela privada do Firefox, Brave, bloqueadores de anúncio) não enviam nada. O público real é maior que o mostrado.
- **Para testar no tempo real:** aba anônima do **Chrome** (ou o celular de outra pessoa), clicar em **Aceitar**, interagir e esperar até 1 min. Navegador marcado com `?interno=1` não aparece, de propósito.
- **"Média por conversão" é distorcida por valores muito altos.** Olhe também as **faixas**.
- **Testes:** os primeiros dias (02 e 03/11) têm muitos testes de configuração, e alguns entraram antes de o filtro de tráfego interno ficar ativo. Visitas dos **Estados Unidos** nesse período são provavelmente robôs ou testes automatizados (Chrome no Linux, em inglês, em data center); desde 2026-11-04 o site não carrega o GA para eles.
- **Eventos principais** só contam a partir da criação (2026-11-03), sem efeito retroativo.
- **Dimensões e métricas novas** levam até 24-48 h para aparecer.

## Validação completa

Feita em 2026-11-03. Para repetir, rode os comandos de cada linha.

| Item | Como foi validado | Resultado |
|---|---|---|
| Site publicado | `curl` no endereço público e no `og.png`/`og.jpg` | ✅ HTTP 200. Conteúdo publicado idêntico ao `index.html` local. |
| GitHub Pages | `gh api repos/andreyoshimura/remessa-japao/pages` | ✅ `built`, HTTPS forçado, branch `main` raiz, repositório público |
| GA no site | Busca por `G-HRC1WBVL2V`, `traffic_type`, `valor_reais`, `cotacao_fonte` no HTML publicado | ✅ presentes |
| Search Console | Meta tag no HTML publicado + Inspeção de URL | ✅ verificada; "O URL está no Google" |
| Prévia de links | Depurador do Facebook | ✅ imagem e título corretos |
| Segredos fora do Git | `git ls-files` + busca por tokens e chaves em **todo** o histórico (`git log -p --all`) | ✅ 0 ocorrências |
| Credenciais locais | `ls -l ~/.config/radar-nihon` | ✅ pasta `700`, arquivos `600` |
| `.gitignore` | `git check-ignore` com nomes de credencial de exemplo | ✅ bloqueia credenciais, deixa passar `.mcp.json` e `scripts/` |
| Configuração do GA | `scripts/ga-status.sh` e `scripts/ga-definicoes.sh` | ✅ eventos principais, Signals desligado, retenção 14 meses, 5 dimensões e 3 métricas |
| Captura do valor | Navegador sem tela, lendo o `dataLayer` | ✅ abrir sem mexer: 0 eventos. ¥100.000 → ¥150.000: 2 conversões com valor em ienes, reais e cotação. Cotação digitada: `cotacao_fonte = manual`. |
| Data API | `scripts/ga-relatorio.py` | ✅ responde com os dados da propriedade |
| MCP oficial | Conversa JSON-RPC direta com o `analytics-mcp` (9 ferramentas; `run_report` testado) | ✅ |
| Filtro de tráfego interno | Painel do GA (não há API) | ✅ ativo. Firefox e celular marcados com `?interno=1`. |

## Vantagens do que foi feito

**Para o negócio**
- **Saber quanto o público converte.** Valor em ienes e em reais por conversão, faixas, média e cotação. É a base para negociar com serviços de remessa (Wise e outros), escolher conteúdo e provar o tamanho do público.
- **Saber o que traz gente.** Origem de cada visita (Instagram bio, Facebook, WhatsApp, Google), com os eventos principais medindo o que importa: compartilhar e seguir nas redes.
- **Medir o boca a boca.** Cada compartilhamento no WhatsApp leva `utm_source=whatsapp`, então as visitas que ele gera aparecem separadas. O valor no momento do compartilhamento também é guardado.
- **Aparecer no Google.** O Search Console está verificado, o site já está indexado, e as buscas que trazem gente vão aparecer no GA.

**Para a qualidade dos dados**
- **Dados limpos:**
  - as suas visitas não contam (filtro de tráfego interno);
  - o valor padrão da página não infla as conversões;
  - o Google Signals desligado evita que o GA esconda números num site pequeno.
- **Dados que não se perdem com o tempo:** retenção de 14 meses, e a cotação guardada em cada conversão permite comparar períodos de câmbio diferentes.

**Para o trabalho do dia a dia**
- **Sem abrir o painel.** Relatórios por script ou perguntando ao Claude Code (MCP oficial).
- **Administração repetível.** Os scripts mostram antes o que vão mudar e podem ser rodados de novo sem estragar nada.
- **Tudo documentado.** Passo a passo para refazer em outra máquina.

**Para a segurança e a privacidade**
- **Sem senha permanente.** Acesso pela API com token da sua conta (ADC com cliente OAuth interno), revogável a qualquer momento.
- **Credenciais fora do repositório.** Elas nunca entram no repositório público, que tem bloqueio no `.gitignore` e foi verificado em todo o histórico.
- **LGPD.** Aviso de cookies com Consent Mode v2. Nenhum dado pessoal vai para o GA, só valores e cliques.

## Pendências

- [x] Eventos principais `compartilhar_whatsapp` e `clique_rede_social`: criados pela Admin API em 2026-11-03.
- [x] Métrica **Valor em ienes** (`valor_ienes`) criada.
- [x] Dimensão "Valor ienes" criada por engano: arquivada (confirmado pela API).
- [x] Retenção de dados de eventos: **14 meses** (confirmado pela API).
- [x] **Google Signals** desligado (confirmado pela API).
- [x] `close_convert_lead` e `qualify_lead` deixaram de ser eventos principais.
- [x] Search Console: o site já está no Google (confirmado na Inspeção de URL em 2026-11-03).
- [x] `?interno=1` aberto no Firefox e no celular (2026-11-03). Repetir em navegador ou aparelho novo, ou depois de limpar os dados do navegador.
- [x] `?interno=1` aberto em todos os aparelhos de quem testa (2026-11-04, depois da análise que achou visitas internas não marcadas). Repetir em aparelho novo ou depois de limpar os dados do navegador.
- [ ] (Depois do alerta/webhook) Contador anônimo de **aceite × recusa** dos cookies pelo webhook do n8n, sem dado pessoal, para saber o tamanho do "piso" do GA.
- [x] Robôs fora do GA (2026-11-04). Seção **Japão** e `GA_EXCLUIR_CIDADES` no relatório. Search Console API ligada (`sc-relatorio.py`).
- [ ] Conferir de vez em quando se o filtro **Internal Traffic** continua **Ativo**. Manual, porque não há API para isso.
- [ ] (Opcional) Links de **YouTube** e **WhatsApp** para o rodapé.

## Possíveis próximos passos

- **Captar contatos:** ligar o formulário de alerta de câmbio (`WEBHOOK_URL`, por exemplo um fluxo n8n que salva numa planilha) ou um botão "Falar no WhatsApp" para o seu número.
- **Afiliado:** preencher `AFFILIATE_URL` para mostrar o botão da Wise.
- **Relatórios pelo MCP:** perguntar ao Claude Code coisas como "quantos compartilhamentos esta semana?" ou "de onde vieram as visitas do mês?".
