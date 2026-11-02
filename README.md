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
- **"Mandar esta conversão no WhatsApp"**: abre o WhatsApp com o texto da conversão e o link do site.
- Rodapé com as redes sociais e o link "Preferências de cookies".
- Funciona embutido em outro site (iframe ou `?embed=1`): esconde topo e rodapé e ajusta a altura do iframe.
- Recursos prontos, mas **desligados**: botão de afiliado (Wise) e formulário "Me avise quando o iene subir" (leads via webhook).

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O site inteiro: HTML, CSS e JavaScript, sem dependências além da fonte do Google Fonts. |
| `og.jpg` | Imagem de prévia de links (1200×630, ~127 KB) usada por WhatsApp, Facebook, Instagram e X. |
| `docs/analytics.md` | GA4, Search Console, prévia de links e validação. |
| `.gitignore` | Mantém fora do repositório o arquivo de instrução original e a pasta `.claude`. |

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
- Se mudar título, descrição ou `og.jpg`, aumente o `v=` do link do WhatsApp no código (hoje `v=3`).

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
