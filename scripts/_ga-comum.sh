#!/bin/sh
# Funções comuns dos scripts de administração do GA4. Sem segredos:
# o token vem das Application Default Credentials guardadas FORA do repositório.
#
# Variáveis (todas opcionais):
#   GA_PROPERTY      ID numérico da propriedade (padrão: 561947228, "Calculadora remessa")
#   GA_QUOTA_PROJECT projeto do Google Cloud usado para cota (padrão: radar-nihon-analytics)
#   CLOUDSDK_CONFIG  pasta de configuração do gcloud (padrão: ~/.config/radar-mercado/radar-nihon/gcloud)
#   GCLOUD           caminho do gcloud (padrão: ~/.local/opt/google-cloud-sdk/bin/gcloud)

set -eu

GA_PROPERTY="${GA_PROPERTY:-561947228}"
GA_QUOTA_PROJECT="${GA_QUOTA_PROJECT:-radar-nihon-analytics}"
export CLOUDSDK_CONFIG="${CLOUDSDK_CONFIG:-$HOME/.config/radar-mercado/radar-nihon/gcloud}"
GCLOUD="${GCLOUD:-$HOME/.local/opt/google-cloud-sdk/bin/gcloud}"
ADMIN="https://analyticsadmin.googleapis.com"
PROP="properties/$GA_PROPERTY"

APLICAR=0
for arg in "$@"; do
  case "$arg" in
    --aplicar) APLICAR=1 ;;
    -h|--help) sed -n '2,/^$/p' "$0"; exit 0 ;;
    *) echo "Opção desconhecida: $arg" >&2; exit 2 ;;
  esac
done

TOKEN="$("$GCLOUD" auth application-default print-access-token 2>/dev/null)" || {
  echo "Sem credencial ADC. Rode: radar-nihon-adc-login" >&2; exit 1; }

# api MÉTODO URL [CORPO_JSON]  -> imprime a resposta; falha se HTTP >= 400
api() {
  _m="$1"; _u="$2"; _b="${3:-}"
  _out="$(mktemp)"
  if [ -n "$_b" ]; then
    _code="$(curl -sS -o "$_out" -w '%{http_code}' -X "$_m" "$_u" \
      -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $GA_QUOTA_PROJECT" \
      -H "Content-Type: application/json" -d "$_b")"
  else
    _code="$(curl -sS -o "$_out" -w '%{http_code}' -X "$_m" "$_u" \
      -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: $GA_QUOTA_PROJECT")"
  fi
  cat "$_out"; rm -f "$_out"
  [ "$_code" -lt 400 ] || { echo "\nHTTP $_code em $_m $_u" >&2; return 1; }
}

# json EXPRESSÃO_PYTHON  -> lê JSON do stdin em "d" e imprime o resultado
json() { python3 -I -c "import json,sys; d=json.load(sys.stdin); print($1)"; }
