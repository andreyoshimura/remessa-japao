#!/bin/sh
# Resumo, só leitura, da configuração do GA4 que o docs/analytics.md acompanha:
# eventos principais, Google Signals, retenção, definições personalizadas
# e eventos recebidos nos últimos 28 dias.
#
# Uso: scripts/ga-status.sh

. "$(dirname "$0")/_ga-comum.sh"

echo "Propriedade: $PROP"
echo
echo "Eventos principais:"
api GET "$ADMIN/v1beta/$PROP/keyEvents?pageSize=200" \
  | json "'\n'.join('  - '+k['eventName']+' ('+k.get('countingMethod','')+')' for k in d.get('keyEvents',[])) or '  (nenhum)'"
echo
printf "Google Signals: "
api GET "$ADMIN/v1alpha/$PROP/googleSignalsSettings" | json "d.get('state')"
printf "Retenção de eventos: "
api GET "$ADMIN/v1beta/$PROP/dataRetentionSettings" | json "d.get('eventDataRetention')"
echo
echo "Dimensões personalizadas:"
api GET "$ADMIN/v1beta/$PROP/customDimensions?pageSize=200" \
  | json "'\n'.join('  - '+x['displayName'].strip()+' -> '+x['parameterName']+' ('+x['scope']+')' for x in d.get('customDimensions',[])) or '  (nenhuma)'"
echo "Métricas personalizadas:"
api GET "$ADMIN/v1beta/$PROP/customMetrics?pageSize=200" \
  | json "'\n'.join('  - '+x['displayName']+' -> '+x['parameterName']+' ('+x['scope']+')' for x in d.get('customMetrics',[])) or '  (nenhuma)'"
echo
echo "Filtros de dados: não existem na Admin API; conferir no painel"
echo "  (Administrador > Coleta e modificação de dados > Filtros de dados)."
echo
echo "Eventos recebidos (28 dias):"
api POST "https://analyticsdata.googleapis.com/v1beta/$PROP:runReport" \
  '{"dateRanges":[{"startDate":"28daysAgo","endDate":"today"}],"dimensions":[{"name":"eventName"}],"metrics":[{"name":"eventCount"}],"orderBys":[{"metric":{"metricName":"eventCount"},"desc":true}]}' \
  | json "'\n'.join('  - '+r['dimensionValues'][0]['value']+': '+r['metricValues'][0]['value'] for r in d.get('rows',[])) or '  (nenhum)'"
