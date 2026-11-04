#!/bin/sh
# Marca como eventos principais (key events) do GA4:
#   compartilhar_whatsapp, clique_rede_social
# Método de contagem: uma vez por evento (ONCE_PER_EVENT).
#
# Uso:
#   scripts/ga-eventos-principais.sh            mostra o que faria (não muda nada)
#   scripts/ga-eventos-principais.sh --aplicar  cria os que faltam
#
# Idempotente: eventos que já são principais ficam como estão.

. "$(dirname "$0")/_ga-comum.sh"

EVENTOS="compartilhar_whatsapp clique_rede_social"

atuais="$(api GET "$ADMIN/v1beta/$PROP/keyEvents?pageSize=200" | json "' '.join(k['eventName'] for k in d.get('keyEvents',[]))")"
echo "Propriedade: $PROP"
echo "Eventos principais hoje: ${atuais:-(nenhum)}"
echo

faltam=""
for e in $EVENTOS; do
  case " $atuais " in
    *" $e "*) echo "  = $e  (já é evento principal, nada a fazer)" ;;
    *)        echo "  + $e  (será marcado como evento principal, contagem: uma vez por evento)"; faltam="$faltam $e" ;;
  esac
done

[ -n "$faltam" ] || { echo; echo "Nada a mudar."; exit 0; }
if [ "$APLICAR" -ne 1 ]; then
  echo; echo "Simulação: nada foi alterado. Para aplicar, rode de novo com --aplicar."; exit 0
fi

echo
for e in $faltam; do
  api POST "$ADMIN/v1beta/$PROP/keyEvents" "{\"eventName\":\"$e\",\"countingMethod\":\"ONCE_PER_EVENT\"}" \
    | json "'  criado: '+d['eventName']+'  ('+d['name']+')'"
done
