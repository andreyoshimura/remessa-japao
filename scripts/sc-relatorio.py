#!/usr/bin/env python3
"""Buscas do Google que mostram o conversor (só leitura), pela Search Console API.

Uso:
  python3 -I scripts/sc-relatorio.py                  últimos 28 dias, todos os países
  python3 -I scripts/sc-relatorio.py jpn              só o Japão (código ISO de 3 letras)
  python3 -I scripts/sc-relatorio.py jpn 2026-11-01   só o Japão, a partir da data

Sem segredos: usa as mesmas Application Default Credentials do ga-relatorio.py, com o
escopo webmasters.readonly (veja docs/analytics.md, "Conexão pela API").
O Search Console tem atraso de 2 a 3 dias e esconde consultas raras (privacidade).
"""
import datetime, json, os, subprocess, sys, urllib.parse, urllib.request

SITE = os.environ.get("SC_SITE", "https://andreyoshimura.github.io/remessa-japao/")
PROJETO_COTA = os.environ.get("GA_QUOTA_PROJECT", "radar-nihon-analytics")
GCLOUD = os.environ.get("GCLOUD", os.path.expanduser("~/.local/opt/google-cloud-sdk/bin/gcloud"))
os.environ.setdefault("CLOUDSDK_CONFIG", os.path.expanduser("~/.config/radar-mercado/radar-nihon/gcloud"))

pais = sys.argv[1].lower() if len(sys.argv) > 1 and sys.argv[1] != "-" else ""
hoje = datetime.date.today()
inicio = sys.argv[2] if len(sys.argv) > 2 else str(hoje - datetime.timedelta(days=28))
fim = str(hoje)

try:
    TOKEN = subprocess.run([GCLOUD, "auth", "application-default", "print-access-token"],
                           capture_output=True, text=True, check=True).stdout.strip()
except Exception:
    sys.exit("Sem credencial ADC. Rode: radar-nihon-adc-login")


def consulta(dims, limite=25):
    corpo = {"startDate": inicio, "endDate": fim, "dimensions": dims, "rowLimit": limite}
    if pais:
        corpo["dimensionFilterGroups"] = [{"filters": [{"dimension": "country", "operator": "equals", "expression": pais}]}]
    url = ("https://searchconsole.googleapis.com/webmasters/v3/sites/"
           + urllib.parse.quote(SITE, safe="") + "/searchAnalytics/query")
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {TOKEN}", "x-goog-user-project": PROJETO_COTA,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r).get("rows", [])
    except urllib.error.HTTPError as e:
        corpo = e.read().decode()[:300]
        if e.code == 403 and "insufficient" in corpo.lower():
            sys.exit("Falta o escopo webmasters.readonly. Rode de novo: radar-nihon-adc-login")
        sys.exit(f"Erro {e.code} da Search Console API: {corpo}")


def tabela(titulo, cab, linhas):
    print(f"\n## {titulo}\n")
    if not linhas:
        print("(sem dados no período: o site ainda não apareceu em buscas, ou as consultas são raras demais)")
        return
    print("| " + " | ".join(cab) + " |")
    print("|" + "|".join("---" for _ in cab) + "|")
    for l in linhas:
        print("| " + " | ".join(str(c) for c in l) + " |")


def linha(r):
    return [r["clicks"], r["impressions"], f"{r['ctr'] * 100:.1f}%".replace(".", ","), f"{r['position']:.1f}".replace(".", ",")]


print(f"# Buscas no Google: conversor\n\nPeríodo: {inicio} a {fim}. País: {pais.upper() or 'todos'}.")
cab = ["Cliques", "Impressões", "CTR", "Posição média"]
tabela("Consultas", ["Consulta"] + cab, [[r["keys"][0]] + linha(r) for r in consulta(["query"])])
if not pais:
    tabela("Países", ["País"] + cab, [[r["keys"][0].upper()] + linha(r) for r in consulta(["country"], 15)])
tabela("Aparelho", ["Aparelho"] + cab, [[r["keys"][0]] + linha(r) for r in consulta(["device"])])
tabela("Por dia", ["Dia"] + cab, [[r["keys"][0]] + linha(r) for r in consulta(["date"], 60)])
