#!/usr/bin/env python3
"""Relatório do conversor (só leitura) pela Google Analytics Data API.

Uso:
  python3 -I scripts/ga-relatorio.py                 desde o lançamento (2026-11-02) até hoje
  python3 -I scripts/ga-relatorio.py 7daysAgo        últimos 7 dias
  python3 -I scripts/ga-relatorio.py 2026-11-03 today

Variável opcional GA_EXCLUIR_CIDADES="Cidade A,Cidade B": mostra também os números sem essas
cidades (ex.: onde moram os testadores). Fica só no ambiente, nunca no repositório (público).

Sem segredos: o token vem das Application Default Credentials guardadas fora do
repositório (veja docs/analytics.md, "Conexão pela API"). Datas no fuso da
propriedade (Ásia/Tóquio). O tráfego interno já vem excluído pelo filtro do GA.
"""
import json, os, subprocess, sys, urllib.request

PROPRIEDADE = os.environ.get("GA_PROPERTY", "561947228")
PROJETO_COTA = os.environ.get("GA_QUOTA_PROJECT", "radar-nihon-analytics")
GCLOUD = os.environ.get("GCLOUD", os.path.expanduser("~/.local/opt/google-cloud-sdk/bin/gcloud"))
os.environ.setdefault("CLOUDSDK_CONFIG", os.path.expanduser("~/.config/radar-mercado/radar-nihon/gcloud"))
# A captura completa do valor (valor_reais, cotacao, sem o valor padrão da página) começou aqui
# (publicada em 03/11 às ~22h no Brasil, que já é 04/11 no fuso da propriedade):
INICIO_CAPTURA_NOVA = "2026-11-04"  # no fuso do GA (Tóquio); 03/11 à noite no Brasil

inicio = sys.argv[1] if len(sys.argv) > 1 else "2026-11-02"
fim = sys.argv[2] if len(sys.argv) > 2 else "today"

try:
    TOKEN = subprocess.run([GCLOUD, "auth", "application-default", "print-access-token"],
                           capture_output=True, text=True, check=True).stdout.strip()
except Exception:
    sys.exit("Sem credencial ADC. Rode: radar-nihon-adc-login")


def relatorio(dims, mets, filtro=None, ordem=None, periodo=None, limite=50):
    corpo = {"dateRanges": [{"startDate": (periodo or (inicio, fim))[0], "endDate": (periodo or (inicio, fim))[1]}],
             "dimensions": [{"name": d} for d in dims], "metrics": [{"name": m} for m in mets], "limit": limite}
    if filtro:
        corpo["dimensionFilter"] = filtro
    if ordem:
        corpo["orderBys"] = [ordem]
    req = urllib.request.Request(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPRIEDADE}:runReport",
        data=json.dumps(corpo).encode(), method="POST",
        headers={"Authorization": f"Bearer {TOKEN}", "x-goog-user-project": PROJETO_COTA,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    return [([v["value"] for v in row.get("dimensionValues", [])],
             [float(v["value"]) for v in row["metricValues"]]) for row in d.get("rows", [])]


def evento(nomes):
    return {"filter": {"fieldName": "eventName", "inListFilter": {"values": nomes}}}


def ordem_metrica(m):
    return {"metric": {"metricName": m}, "desc": True}


def n(x, casas=0):
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tabela(titulo, cab, linhas):
    print(f"\n## {titulo}\n")
    if not linhas:
        print("(sem dados no período)")
        return
    print("| " + " | ".join(cab) + " |")
    print("|" + "|".join("---" for _ in cab) + "|")
    for l in linhas:
        print("| " + " | ".join(str(c) for c in l) + " |")


print(f"# Relatório do conversor iene ⇄ real\n\nPeríodo: {inicio} a {fim} (fuso Ásia/Tóquio). Tráfego interno excluído.")

# 1. Visão geral
t = relatorio([], ["activeUsers", "newUsers", "sessions", "screenPageViews", "engagementRate",
                   "averageSessionDuration", "eventCount", "keyEvents"])
if t:
    m = t[0][1]
    tabela("Visão geral", ["Métrica", "Valor"], [
        ["Pessoas (usuários ativos)", n(m[0])], ["Pessoas novas", n(m[1])], ["Visitas (sessões)", n(m[2])],
        ["Páginas vistas", n(m[3])], ["Taxa de engajamento", n(m[4] * 100, 1) + "%"],
        ["Tempo médio por visita", f"{int(m[5] // 60)} min {int(m[5] % 60)} s"],
        ["Eventos", n(m[6])], ["Eventos principais (compartilhar + redes)", n(m[7])]])

# 2. Por dia
tabela("Por dia", ["Dia", "Pessoas", "Visitas", "Eventos principais"],
       [[f"{d[0][6:]}/{d[0][4:6]}", n(m[0]), n(m[1]), n(m[2])] for d, m in
        sorted(relatorio(["date"], ["activeUsers", "sessions", "keyEvents"]))])

# 3. De onde vieram
tabela("De onde vieram", ["Origem / mídia", "Visitas", "Pessoas", "Eventos principais"],
       [[d[0], n(m[0]), n(m[1]), n(m[2])] for d, m in
        relatorio(["sessionSourceMedium"], ["sessions", "activeUsers", "keyEvents"], ordem=ordem_metrica("sessions"))])

# 4. Aparelho e país
tabela("Aparelho", ["Aparelho", "Pessoas", "Visitas"],
       [[d[0], n(m[0]), n(m[1])] for d, m in relatorio(["deviceCategory"], ["activeUsers", "sessions"], ordem=ordem_metrica("activeUsers"))])
tabela("País", ["País", "Pessoas", "Visitas"],
       [[d[0], n(m[0]), n(m[1])] for d, m in relatorio(["country"], ["activeUsers", "sessions"], ordem=ordem_metrica("activeUsers"))])
tabela("Cidade", ["Cidade", "País", "Pessoas", "Visitas"],
       [[d[0], d[1], n(m[0]), n(m[1])] for d, m in
        relatorio(["city", "country"], ["activeUsers", "sessions"], ordem=ordem_metrica("sessions"), limite=15)])

# 4b. Japão: o público que faz o projeto faturar em iene
JAPAO = {"filter": {"fieldName": "country", "stringFilter": {"value": "Japan"}}}
def e_(*fs):
    return {"andGroup": {"expressions": list(fs)}}
t = relatorio([], ["activeUsers", "sessions", "engagementRate", "keyEvents"], filtro=JAPAO)
mj = t[0][1] if t else [0, 0, 0, 0]
tabela("Japão (métrica principal)", ["Métrica", "Valor"], [
    ["Pessoas no Japão", n(mj[0])], ["Visitas do Japão", n(mj[1])],
    ["Taxa de engajamento", n(mj[2] * 100, 1) + "%"], ["Eventos principais", n(mj[3])]])
if mj[1]:
    tabela("Japão: de onde vieram", ["Origem / mídia", "Visitas", "Pessoas"],
           [[d[0], n(m[0]), n(m[1])] for d, m in
            relatorio(["sessionSourceMedium"], ["sessions", "activeUsers"], filtro=JAPAO, ordem=ordem_metrica("sessions"))])
    tabela("Japão: cidades", ["Cidade", "Pessoas", "Visitas"],
           [[d[0], n(m[0]), n(m[1])] for d, m in
            relatorio(["city"], ["activeUsers", "sessions"], filtro=JAPAO, ordem=ordem_metrica("sessions"), limite=15)])
    tabela("Japão: ações", ["Evento", "Vezes", "Pessoas"],
           [[d[0], n(m[0]), n(m[1])] for d, m in
            relatorio(["eventName"], ["eventCount", "totalUsers"],
                      filtro=e_(JAPAO, evento(["conversao", "inverter", "compartilhar_whatsapp", "clique_afiliado", "clique_rede_social"])),
                      ordem=ordem_metrica("eventCount"))])

# 4c. Sem as cidades dos testadores (opcional, via ambiente)
EXCL = [c.strip() for c in os.environ.get("GA_EXCLUIR_CIDADES", "").split(",") if c.strip()]
if EXCL:
    SEM = {"notExpression": {"filter": {"fieldName": "city", "inListFilter": {"values": EXCL}}}}
    t = relatorio([], ["activeUsers", "sessions", "keyEvents"], filtro=SEM)
    ms = t[0][1] if t else [0, 0, 0]
    tabela(f"Sem as {len(EXCL)} cidade(s) de GA_EXCLUIR_CIDADES", ["Métrica", "Valor"],
           [["Pessoas", n(ms[0])], ["Visitas", n(ms[1])], ["Eventos principais", n(ms[2])]])

# 5. Cliques e ações
tabela("Cliques e ações", ["Evento", "Vezes", "Pessoas"],
       [[d[0], n(m[0]), n(m[1])] for d, m in relatorio(["eventName"], ["eventCount", "totalUsers"], ordem=ordem_metrica("eventCount"))])
tabela("Redes sociais clicadas", ["Rede", "Cliques", "Pessoas"],
       [[d[0], n(m[0]), n(m[1])] for d, m in relatorio(["customEvent:rede"], ["eventCount", "totalUsers"], filtro=evento(["clique_rede_social"]))])

# 6. Valor convertido
def bloco_valor(titulo, periodo):
    linhas = relatorio(["customEvent:direcao"], ["eventCount", "totalUsers", "customEvent:valor_ienes", "customEvent:valor_reais"],
                       filtro=evento(["conversao"]), periodo=periodo)
    out = []
    for d, m in linhas:
        if not d[0] or d[0] == "(not set)":
            d = ["(versão antiga, sem direção)"]
        media = m[2] / m[0] if m[0] else 0
        out.append([d[0], n(m[0]), n(m[1]), "¥" + n(m[2]), "¥" + n(media), ("R$ " + n(m[3], 2)) if m[3] else "—"])
    tabela(titulo, ["Direção", "Conversões", "Pessoas", "Total em ienes", "Média por conversão", "Total em reais"], out)

bloco_valor("Valor convertido (período inteiro)", None)
if inicio < INICIO_CAPTURA_NOVA:
    bloco_valor(f"Valor convertido só com a captura nova (desde {INICIO_CAPTURA_NOVA})", (INICIO_CAPTURA_NOVA, fim))

tabela("Faixas de valor em ienes (conversões)", ["Faixa", "Conversões", "Pessoas", "Total em ienes"],
       [[d[0], n(m[0]), n(m[1]), "¥" + n(m[2])] for d, m in
        sorted(relatorio(["customEvent:faixa_ienes"], ["eventCount", "totalUsers", "customEvent:valor_ienes"], filtro=evento(["conversao"])))
        if d[0] and d[0] != "(not set)"])
tabela("Valores escolhidos nos botões rápidos", ["Faixa", "Cliques", "Total em ienes"],
       [[d[0], n(m[0]), "¥" + n(m[1])] for d, m in
        sorted(relatorio(["customEvent:faixa_ienes"], ["eventCount", "customEvent:valor_ienes"], filtro=evento(["chip_valor"])))
        if d[0] and d[0] != "(not set)"])
tabela("Valor no momento do compartilhamento no WhatsApp", ["Faixa", "Compartilhamentos", "Total em ienes"],
       [[d[0], n(m[0]), "¥" + n(m[1])] for d, m in
        sorted(relatorio(["customEvent:faixa_ienes"], ["eventCount", "customEvent:valor_ienes"], filtro=evento(["compartilhar_whatsapp"])))
        if d[0] and d[0] != "(not set)"])
tabela("Fonte da cotação usada", ["Fonte", "Conversões", "Cotação média (R$ por ¥1)"],
       [[d[0], n(m[0]), n(m[1] / m[0], 5) if m[0] else "—"] for d, m in
        relatorio(["customEvent:cotacao_fonte"], ["eventCount", "customEvent:cotacao"], filtro=evento(["conversao"]))
        if d[0] and d[0] != "(not set)"])

print("\nObservações:")
print(f"- Antes de {INICIO_CAPTURA_NOVA} toda visita gerava uma conversão de ¥100.000 sozinha (valor padrão da página),")
print("  conversões repetidas na mesma faixa não eram registradas e não havia valor em reais nem cotação.")
print("- Dimensões e métricas personalizadas só valem a partir do registro e podem levar até 24-48 h para aparecer.")
