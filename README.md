# Conversor iene ↔ real

Converte ienes em reais e reais em ienes com a cotação do dia (AwesomeAPI, com a PTAX do Banco Central como reserva).

Site: https://andreyoshimura.github.io/remessa-japao/

- Abrir já na direção reais → ienes: `?de=brl`
- Para ativar o botão de afiliado e o formulário de alerta de câmbio, preencha `AFFILIATE_URL` e `WEBHOOK_URL` no bloco `CONFIG` do `index.html`.

O Google Analytics 4 (`GA_ID` no `CONFIG`) só grava cookies depois que o visitante aceita o aviso. Eventos enviados: `conversao`, `chip_valor`, `inverter`, `outra_cotacao`, `compartilhar_whatsapp` e `clique_afiliado`, com os parâmetros `direcao`, `faixa_ienes` e `ref`. O link compartilhado no WhatsApp leva `utm_source=whatsapp&utm_medium=compartilhamento`.
