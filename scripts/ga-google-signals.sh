#!/bin/sh
# Desliga o Google Signals (indicadores do Google) da propriedade GA4.
# Motivo: num site pequeno ele ativa limites que escondem dados nos relatórios,
# e o site nega o consentimento de anúncios de qualquer forma.
#
# Uso:
#   scripts/ga-google-signals.sh            mostra o estado (não muda nada)
#   scripts/ga-google-signals.sh --aplicar  desliga, se estiver ligado
#
# Usa a Admin API v1alpha (googleSignalsSettings ainda não existe na v1beta).

. "$(dirname "$0")/_ga-comum.sh"

URL="$ADMIN/v1alpha/$PROP/googleSignalsSettings"
estado="$(api GET "$URL" | json "d.get('state','?')")"
echo "Propriedade: $PROP"
echo "Google Signals hoje: $estado"

if [ "$estado" = "GOOGLE_SIGNALS_DISABLED" ]; then
  echo "Já está desligado. Nada a mudar."; exit 0
fi

echo "  ~ state: $estado -> GOOGLE_SIGNALS_DISABLED"
if [ "$APLICAR" -ne 1 ]; then
  echo; echo "Simulação: nada foi alterado. Para aplicar, rode de novo com --aplicar."; exit 0
fi

api PATCH "$URL?updateMask=state" '{"state":"GOOGLE_SIGNALS_DISABLED"}' \
  | json "'  novo estado: '+d['state']"
