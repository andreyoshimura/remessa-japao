# Calculadora de remessa Japão → Brasil

Mostra quanto da remessa em ienes fica com o banco, com a cotação do dia.

Site: https://andreyoshimura.github.io/remessa-japao/

Para ativar o botão de afiliado e o formulário de leads, preencha `AFFILIATE_URL` e `WEBHOOK_URL` no bloco `CONFIG` do `index.html`.

O Google Analytics 4 (`GA_ID` no `CONFIG`) só grava cookies depois que o visitante aceita o aviso. Eventos enviados: `calculo`, `chip_valor`, `abrir_ajustes`, `compartilhar_whatsapp` e `clique_afiliado`, com os parâmetros `faixa_ienes` e `ref`. O link compartilhado no WhatsApp leva `utm_source=whatsapp&utm_medium=compartilhamento`.
