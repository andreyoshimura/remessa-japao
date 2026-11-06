# Conversor iene ⇄ real

Conversor de ienes para reais (e de reais para ienes) com a cotação do dia, feito para brasileiros no Japão. Página única, sem cadastro, publicada no GitHub Pages.

**Site:** https://andreyoshimura.github.io/remessa-japao/
**Redes:** [Instagram](https://www.instagram.com/radarnihon/) · [TikTok](https://www.tiktok.com/@radar.nihon) · [Facebook](https://www.facebook.com/profile.php?id=61595911931098)

> O repositório se chama `remessa-japao` porque começou como calculadora de remessa. O nome foi mantido para não quebrar links já compartilhados.

---

## Sumário

1. [O que o site faz](#o-que-o-site-faz)
2. [Arquivos](#arquivos)
3. [Configuração (bloco CONFIG)](#configuração-bloco-config)
4. [Parâmetros de URL](#parâmetros-de-url)
5. [Cotação](#cotação)
6. [Design](#design)
7. [Como publicar uma alteração](#como-publicar-uma-alteração)
8. [Privacidade](#privacidade)
9. [Histórico](#histórico)

Analytics, Search Console, prévia de links e checklist de validação: **[docs/analytics.md](docs/analytics.md)**.

---

## O que o site faz

- Converte **¥ → R$** e **R$ → ¥**. O botão redondo ⇅ inverte a direção e usa o resultado atual como novo valor.
- Botões de valor rápido: ¥10 mil a ¥200 mil, ou R$ 100 a R$ 5.000.
- Mostra a cotação nos dois sentidos (¥1 = R$ … · R$ 1 = ¥ …) e a fonte usada.
- **"Usar outra cotação"**: a pessoa pode digitar a cotação do banco dela.
- **"Mandar esta conversão no WhatsApp"**: abre o WhatsApp com o texto da conversão e o link do site. Se a pessoa estiver em reais → ienes, o link leva `&de=brl` e abre na mesma direção para quem recebe.
- Rodapé com as redes sociais e o link "Preferências de cookies".
- Funciona embutido em outro site (iframe ou `?embed=1`): esconde topo e rodapé e ajusta a altura do iframe.
- Rodapé com link para **`visto.html`**, o checklist "Estou em dia para renovar o visto?".
- Recursos prontos, mas **desligados**: botão de afiliado (Wise) e formulário "Me avise quando o iene subir" (leads via webhook).

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O site inteiro: HTML, CSS e JavaScript, sem dependências além da fonte do Google Fonts. |
| `visto.html` | Checklist "Estou em dia para renovar o visto?": tipo de visto, 6 perguntas (imposto residencial, seguro de saúde, nenkin, renda extra, endereço, cartão de residência), semáforo por item com onde resolver, documentos por visto e fontes oficiais da Imigração (conferidas em 05/11/2026). As respostas não saem do navegador; o GA recebe só o tipo de visto e a contagem de itens por cor. Bloco "Leve seu resultado": lista das pendências no WhatsApp com frase em japonês para mostrar no balcão (`?ref=lista`), cartão de imagem só com as contagens (`?ref=cartao`, gerado no navegador) e convite que envia só o link (`?ref=whatsapp`); cada item amarelo/vermelho mostra a frase do balcão com a orientação "mostre ao atendente"; com item vermelho aparece o aviso "Está devendo? Negocie antes de renovar" (acordo de parcelamento em dia; base: diretriz de cancelamento do permanente); bloco "Siga o Radar Nihon" (evento `clique_rede_social` com `origem: "visto"`). Versões de parceiro por `?p=código` (lista única em `parceiros.js`, usada também pelo conversor: selo "Checklist da … · feito com Radar Nihon", botão para o vídeo do parceiro, `ref` e dimensão `parceiro` no GA; código fora da lista mostra a versão normal). Imagem de prévia própria `og-visto.png`. Reconferir as regras a cada 6 meses. |
| `og.png` | Imagem de prévia do link (1200×630, PNG, ~33 KB) usada por WhatsApp, Facebook, Instagram e X. |
| `parceiros.js` | Lista única de parceiros (`?p=código`) usada pelo conversor e pela `visto.html`: nome, foto, `ref`, canal e vídeo de cada página. Código fora da lista mostra a versão normal. Para tirar a marca de alguém, apagar a linha. |
| `parceiros/` | Fotos dos parceiros, usadas com autorização. |
| `og-visto.png` | Imagem de prévia do link da `visto.html` (1200×630). |
| `sitemap.xml` | Mapa do site com todas as páginas do repositório (hoje: conversor e `visto.html`). Toda página nova entra aqui com `lastmod` atualizado. Enviado na Search Console pela API em 2026-11-05 (sem erros); reenviar quando mudar. Não dá para declarar no `robots.txt`, que só vale na raiz do domínio. |
| `og.jpg` | Imagem de prévia anterior. Fica no repositório para não quebrar prévias antigas em cache. |
| `docs/analytics.md` | GA4, Search Console, prévia de links, validação e conexão pela API. |
| `scripts/` | Scripts da Admin API do GA4 (`ga-status.sh`, `ga-definicoes.sh`, `ga-eventos-principais.sh`, `ga-google-signals.sh`) os relatórios `ga-relatorio.py` (GA, com seção Japão) e `sc-relatorio.py` (buscas do Search Console). Sem segredos. |
| `.mcp.json` | Configura o MCP oficial do Google Analytics no Claude Code. A credencial fica fora do repositório. |
| `.gitignore` | Mantém fora do repositório o arquivo de instrução original, a pasta `.claude` e qualquer credencial (`*.json` exceto `.mcp.json`, `.env`, chaves). |

## Configuração (bloco CONFIG)

Fica no início do `<script>` do `index.html`:

| Campo | Valor atual | Para que serve |
|---|---|---|
| `AFFILIATE_URL` | `""` (desligado) | Link de afiliado. Se preenchido, mostra o botão "Ver quanto chega pela Wise" e o aviso de afiliado. |
| `WEBHOOK_URL` | `""` (desligado) | URL de webhook (ex.: n8n). Se preenchido, mostra o formulário de alerta de câmbio e envia leads e eventos para ele. |
| `REF` | `"github-pages"` | Origem do visitante, enviada ao GA e ao webhook. |
| `GA_ID` | `"G-HRC1WBVL2V"` | ID de medição do Google Analytics 4. Não é segredo. |
| `SOCIAL.instagram` | radarnihon | Ícone no rodapé. |
| `SOCIAL.facebook` | profile 61595911931098 | Ícone no rodapé. |
| `SOCIAL.tiktok` | @radar.nihon | Ícone no rodapé. |
| `SOCIAL.youtube` | `""` | Vazio, por isso não aparece. |
| `SOCIAL.whatsapp` | `""` | Vazio, por isso não aparece. Aceita `https://wa.me/81…` ou link de canal/grupo. |

Cada rede só aparece se o link começar com `https://`.

> **Atenção:** o repositório é público. Não coloque a URL do webhook no `index.html`: qualquer pessoa conseguiria ler e mandar dados falsos para ela. Prefira passar pela URL (`?hook=`) numa página embutida.

## Parâmetros de URL

| Parâmetro | Efeito |
|---|---|
| `?de=brl` | Abre na direção reais → ienes. |
| `?ref=CODIGO` | Define a origem (ex.: `?ref=instagram`, `?ref=parceiro-x`). |
| `?embed=1` | Modo embutido (também ativa sozinho dentro de iframe). |
| `?interno=1` / `?interno=0` | Marca ou desmarca o seu navegador como tráfego interno, que o GA filtra. Ver [docs/analytics.md](docs/analytics.md#tráfego-interno). |
| `?aff=` · `?hook=` · `?ga=` | Sobrescrevem `AFFILIATE_URL`, `WEBHOOK_URL` e `GA_ID` sem editar o arquivo. |
| `?utm_source=…&utm_medium=…` | Atribuição de campanha no GA. O botão do WhatsApp já usa `whatsapp / compartilhamento`. |
| `?v=N` | Só muda o endereço, para forçar o WhatsApp a buscar a prévia nova. Não tem efeito na página. |

## Cotação

1. **AwesomeAPI** (`economia.awesomeapi.com.br/json/last/JPY-BRL`): cotação de mercado, campo `bid`.
2. Se falhar, a reserva é a **PTAX do Banco Central** (`olinda.bcb.gov.br`), tentando os últimos 6 dias para pular fins de semana e feriados.
3. Se as duas falharem, a página pede a cotação manual e envia o evento `cotacao_erro` ao GA.

A página avisa que bancos e casas de câmbio cobram tarifa e margem, então o valor recebido pode ser menor.

**Formato dos números:** tudo em pt-BR. Ienes aparecem como `¥29.028`, porque o formato japonês (`29,028`) parece decimal para quem lê em português.

## Design

- **Paleta:** azul índigo japonês (*ai-zome*) `#1E3557`, com detalhes em vermelho (hinomaru) e verde.
- **Topo:** degradê índigo com padrão de ondas *seigaiha* em SVG.
- **Fonte:** Zen Kaku Gothic New (Google Fonts).
- **Modo escuro:** automático, segue o sistema. As cores ficam em variáveis no `:root`.
- **Responsivo:** coluna de até 500 px, pensada primeiro para o celular.

## Como publicar uma alteração

O GitHub Pages publica a branch `main`, pasta raiz.

```bash
# editar index.html, depois:
git add index.html
git commit -m "Descrição da mudança"
git push

# acompanhar a publicação (fica "built" em cerca de 1 minuto)
gh api repos/andreyoshimura/remessa-japao/pages/builds/latest --jq .status

# conferir o site
curl -s -o /dev/null -w "%{http_code}\n" https://andreyoshimura.github.io/remessa-japao/
```

Antes de publicar:
- `AFFILIATE_URL` e `WEBHOOK_URL` vazios, a menos que seja de propósito.
- **Não remover** a meta tag `google-site-verification`, porque o Search Console perde a verificação.
- Se mudar título, descrição ou `og.png`, aumente o `v=` do link do WhatsApp no código (hoje `v=4`).

## Privacidade

- **Google Analytics com Consent Mode v2.** Sem aceite, nada de cookies, só sinais anônimos. Com aceite, a medição é normal. Anúncios sempre negados.
- **Aviso de cookies** no primeiro acesso, e o link "Preferências de cookies" no rodapé para mudar a escolha.
- **Nenhum dado pessoal vai para o GA:** nem nome, nem telefone, nem e-mail. As regras do Google proíbem.
- **Formulário de leads,** quando ligado: exige caixa de consentimento e envia os dados só para o webhook configurado.

## Histórico

| Data | Commit | Mudança |
|---|---|---|
| 2026-11-02 | `22a3d76` | Primeira versão: calculadora de quanto da remessa fica com o banco. |
| 2026-11-02 | `e6bb24b` | Google Analytics 4 com aviso de cookies e eventos. |
| 2026-11-02 | `79b6844` | Vira conversor simples iene ⇄ real, com botão para inverter. |
| 2026-11-02 | `bb56abd` | Novo design (topo índigo, cartão, etiquetas JPY/BRL) e Instagram no rodapé. |
| 2026-11-02 | `b3ed7d0`, `ff350a0` | TikTok e Facebook no rodapé. |
| 2026-11-02 | `efdae5e` | GA: valor convertido, tráfego interno, escolha de cookies e erro de cotação. |
| 2026-11-02 | `9481d0c` | Verificação do Google Search Console. |
| 2026-11-02 | `dfc426b` | Imagem de prévia (`og.jpg`) e tags Open Graph completas. |
| 2026-11-02 | `0ca3500` | `⇄` no título da prévia, porque o Facebook mostrava `↔` como emoji quebrado. |
| 2026-11-02 | `b09daed` | Nova imagem de prévia `og.png` (fonte dos posts), texto de cookies "sem saber seu nome nem seu contato" e bolinha "ao vivo" só com cotação automática. |
| 2026-11-04 | `f7656ba` | Título, descrição e subtítulo citam "real para iene" (busca nº 1 no Japão); link do WhatsApp mantém a direção (`&de=brl`). |
| 2026-11-04 | `2aa57a2` | Robôs fora do GA; relatório com seção Japão e `GA_EXCLUIR_CIDADES`; `sc-relatorio.py` (Search Console API). |
| 2026-11-05 | `85b6b79` | Conversor com versão de parceiro (`?p=carla`: selo, botão para os vídeos, link para o checklist da parceira); lista única `parceiros.js`; compartilhamentos levam o `p` junto. |
| 2026-11-05 | `4cb6357` | `visto.html`: versões de parceiro por `?p=` (primeira: `?p=carla`, Carla no Japão). |
| 2026-11-05 | `9286509` | `visto.html`: orientação do balcão, aviso "Negocie antes de renovar", textos de seguro e nenkin atrasados, "Siga o Radar Nihon", mensagem do WhatsApp reorganizada. |
| 2026-11-05 | `b752ff3` | `visto.html`: "Leve seu resultado" (lista no WhatsApp com frases em japonês para o balcão, cartão de imagem com as contagens, convite); evento `enviar_resultado`. |
| 2026-11-05 | `1773177` | `visto.html`: imagem de prévia `og-visto.png`, botão do WhatsApp (evento `compartilhar_whatsapp` com `origem: "visto"`); `sitemap.xml` com as duas páginas. |
| 2026-11-05 | `ad97775` | Checklist `visto.html` ("Estou em dia para renovar o visto?") com regras oficiais da Imigração, eventos `checklist_visto` e `checklist_resultado`; link no rodapé do conversor. |
