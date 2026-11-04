#!/bin/sh
# Garante que as definições personalizadas usadas pelo site existam no GA4.
# Parâmetro sem definição não aparece nos relatórios, e o registro NÃO é retroativo:
# só vale para os eventos recebidos depois dele.
#
# Uso:
#   scripts/ga-definicoes.sh            mostra o que falta (não muda nada)
#   scripts/ga-definicoes.sh --aplicar  cria só o que falta
#
# Idempotente: compara pelo nome do parâmetro e não mexe no que já existe.

. "$(dirname "$0")/_ga-comum.sh"

# tipo|parâmetro|nome no GA|unidade (métricas: STANDARD; CURRENCY exige restrictedMetricType de receita/custo)|descrição
DEFINICOES='dim|direcao|Direção||iene_para_real ou real_para_iene
dim|faixa_ienes|Faixa de ienes||Faixa do valor em ienes
dim|ref|Origem||Origem do visitante (?ref=)
dim|rede|Rede Social||Rede clicada no rodapé
dim|cotacao_fonte|Fonte da cotação||awesomeapi, ptax ou manual
met|valor_ienes|Valor em ienes|STANDARD|Valor convertido, em ienes
met|valor_reais|Valor em reais|STANDARD|Valor convertido, em reais (número; CURRENCY exigiria marcar como receita ou custo)
met|cotacao|Cotação usada|STANDARD|Reais por 1 iene usados na conversão'

dims="$(api GET "$ADMIN/v1beta/$PROP/customDimensions?pageSize=200" | json "' '.join(x['parameterName'] for x in d.get('customDimensions',[]))")"
mets="$(api GET "$ADMIN/v1beta/$PROP/customMetrics?pageSize=200" | json "' '.join(x['parameterName'] for x in d.get('customMetrics',[]))")"
echo "Propriedade: $PROP"
echo

faltam=""
IFS_OLD="$IFS"; IFS='
'
for linha in $DEFINICOES; do
  tipo="${linha%%|*}"; resto="${linha#*|}"; param="${resto%%|*}"; resto="${resto#*|}"; nome="${resto%%|*}"; resto="${resto#*|}"; unid="${resto%%|*}"
  if [ "$tipo" = dim ]; then existentes="$dims"; rotulo="dimensão"; else existentes="$mets"; rotulo="métrica ($unid)"; fi
  case " $existentes " in
    *" $param "*) echo "  = $rotulo $param  (já existe)" ;;
    *)            echo "  + $rotulo $param  -> \"$nome\", escopo Evento"; faltam="$faltam
$linha" ;;
  esac
done
IFS="$IFS_OLD"

[ -n "$faltam" ] || { echo; echo "Nada a mudar."; exit 0; }
if [ "$APLICAR" -ne 1 ]; then
  echo; echo "Simulação: nada foi alterado. Para aplicar, rode de novo com --aplicar."; exit 0
fi

echo
IFS='
'
for linha in $faltam; do
  [ -n "$linha" ] || continue
  tipo="${linha%%|*}"; resto="${linha#*|}"; param="${resto%%|*}"; resto="${resto#*|}"; nome="${resto%%|*}"; resto="${resto#*|}"; unid="${resto%%|*}"; desc="${resto#*|}"
  if [ "$tipo" = dim ]; then
    api POST "$ADMIN/v1beta/$PROP/customDimensions" \
      "{\"parameterName\":\"$param\",\"displayName\":\"$nome\",\"description\":\"$desc\",\"scope\":\"EVENT\"}" \
      | json "'  criada dimensão: '+d['parameterName']+' ('+d['name']+')'"
  else
    api POST "$ADMIN/v1beta/$PROP/customMetrics" \
      "{\"parameterName\":\"$param\",\"displayName\":\"$nome\",\"description\":\"$desc\",\"scope\":\"EVENT\",\"measurementUnit\":\"$unid\"}" \
      | json "'  criada métrica: '+d['parameterName']+' ('+d['name']+')'"
  fi
done
IFS="$IFS_OLD"
