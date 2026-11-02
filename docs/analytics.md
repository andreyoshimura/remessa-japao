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
9. [Pendências](#pendências)
10. [Possíveis próximos passos](#possíveis-próximos-passos)

---

## Visão geral

| Item | Valor |
|---|---|
| Conta GA | Remessa Japao |
| Propriedade GA4 | Calculadora remessa (fuso: Japão) |
| Fluxo da Web | Site Github Pages, `https://andreyoshimura.github.io/remessa-japao` |
| ID de medição | `G-HRC1WBVL2V` |
| Medição otimizada | Ativada (visualizações, rolagem, cliques de saída etc.) |
| Search Console | Propriedade por prefixo de URL, verificada por meta tag e vinculada ao GA |

O GA4 é carregado pelo próprio `index.html`, e não pelo snippet padrão do Google, para respeitar o aviso de cookies.

## Eventos enviados ao GA4

| Evento | Quando dispara | Parâmetros |
|---|---|---|
| `page_view` | Abertura da página (automático) | `ref`, `origem` (`pagina`/`embed`) |
| `conversao` | 1,5 s depois de a pessoa parar de digitar, só quando a faixa ou a direção muda | `direcao`, `faixa_ienes`, `valor_ienes`, `ref` |
| `chip_valor` | Clique num valor rápido (¥50 mil, R$ 500…) | `direcao`, `faixa_ienes`, `valor_ienes`, `ref` |
| `inverter` | Clique no botão ⇅ | `direcao`, `faixa_ienes`, `valor_ienes`, `ref` |
| `outra_cotacao` | Abriu "Usar outra cotação" | `direcao`, `faixa_ienes`, `valor_ienes`, `ref` |
| `compartilhar_whatsapp` | Clique em "Mandar esta conversão no WhatsApp" | `direcao`, `faixa_ienes`, `valor_ienes`, `ref` |
| `clique_rede_social` | Clique num ícone do rodapé | os acima + `rede` (`instagram`/`facebook`/`tiktok`/…) |
| `clique_afiliado` | Clique no botão da Wise (quando ligado) | `direcao`, `faixa_ienes`, `valor_ienes`, `ref` |
| `cookies_aceitos` / `cookies_recusados` | Resposta ao aviso de cookies | — |
| `cotacao_erro` | AwesomeAPI e PTAX falharam | — |

**Valores dos parâmetros:**
- `direcao`: `iene_para_real` ou `real_para_iene`.
- `faixa_ienes`: sempre calculada em ienes, nas duas direções. Valores possíveis: `ate_50mil`, `50_100mil`, `100_200mil`, `200_300mil`, `300mil_mais`.
- `valor_ienes`: número inteiro, o valor convertido em ienes.
- `ref`: origem, `github-pages` por padrão, ou o valor de `?ref=`.

**Atribuição do WhatsApp:** o link compartilhado leva `utm_source=whatsapp&utm_medium=compartilhamento`. Em **Aquisição → Aquisição de tráfego** essas visitas aparecem como `whatsapp / compartilhamento`.

## Configuração feita no GA4

Feita à mão em 2026-11-02.

| Onde | O quê | Situação |
|---|---|---|
| Exibição de dados → Definições personalizadas | Dimensão **Direção** → `direcao` (Evento) | ✅ |
| 〃 | Dimensão **Faixa de ienes** → `faixa_ienes` (Evento) | ✅ |
| 〃 | Dimensão **Origem** → `ref` (Evento) | ✅ |
| 〃 | Dimensão **Rede Social** → `rede` (Evento) | ✅ |
| 〃 | Métrica **Valor em ienes** → `valor_ienes` (Evento, Padrão) | ✅ criada (2026-11-02). Se a dimensão "Valor ienes" criada por engano ainda existir, arquivar. |
| Coleta e modificação de dados → Filtros de dados | **Internal Traffic**: excluir `traffic_type = internal`, estado **Ativo** | ✅ |
| Vínculos de produtos → Links do Search Console | Vínculo com `https://andreyoshimura.github.io/remessa-japao/` e o fluxo Site Github Pages | ✅ |
| Exibição de dados → Eventos | ⭐ evento principal em `compartilhar_whatsapp` e `clique_rede_social` | ⏳ os eventos só aparecem na lista ~24 h depois do primeiro disparo |
| Coleta e modificação de dados → Retenção de dados | Eventos: **14 meses** (padrão é 2) | ✅ (2026-11-02) |
| Coleta e modificação de dados → Coleta de dados | **Google Signals desligado**: evita limites que escondem dados num site pequeno, e o site nega consentimento de anúncios de qualquer jeito | ⏳ confirmar |

Os eventos principais `close_convert_lead` e `qualify_lead` foram criados automaticamente pelo objetivo "Gerar leads". O site não envia esses eventos, então dá para tirar a estrela deles.

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

## Google Search Console

- **Propriedade:** prefixo de URL `https://andreyoshimura.github.io/remessa-japao/`. O tipo "Domínio" não funciona para `github.io`.
- **Verificação:** meta tag no `<head>` do `index.html`:
  ```html
  <meta name="google-site-verification" content="BanQ_ppxaXERI9g8SKpXYfudEKwdMDiMg2NF3ZrcAw0" />
  ```
  **Não remover.** O Google confere de tempos em tempos.
- **Vínculo com o GA:** feito. Os dados aparecem em **Relatórios → Aquisição → Search Console** depois que o site começar a aparecer no Google.
- **Recomendado:** em **Inspeção de URL → Solicitar indexação**, para acelerar a entrada no Google.

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

## Pendências

- [ ] Marcar ⭐ em `compartilhar_whatsapp` e `clique_rede_social` em **Administrador → Eventos**, depois que aparecerem (~24 h).
- [x] Métrica **Valor em ienes** (`valor_ienes`) criada.
- [ ] Arquivar a dimensão "Valor ienes" criada por engano, se ainda existir.
- [x] Retenção de dados de eventos: **14 meses**.
- [ ] Desligar o **Google Signals**.
- [ ] Search Console: **Solicitar indexação**.
- [ ] Abrir `?interno=1` em todos os seus navegadores e celulares.
- [ ] (Opcional) Tirar a estrela de `close_convert_lead` e `qualify_lead`.
- [ ] (Opcional) Links de **YouTube** e **WhatsApp** para o rodapé.

## Possíveis próximos passos

- **Captar contatos:** ligar o formulário de alerta de câmbio (`WEBHOOK_URL`, por exemplo um fluxo n8n que salva numa planilha) ou um botão "Falar no WhatsApp" para o seu número.
- **Afiliado:** preencher `AFFILIATE_URL` para mostrar o botão da Wise.
- **MCP do Google Analytics:** é só leitura. Permitiria perguntar daqui coisas como "quantos compartilhamentos esta semana?". Exige projeto no Google Cloud, a API ativada e uma credencial OAuth.
