from bs4 import BeautifulSoup
import os

arquivo_html = "Suplementos_ comprar suplementos alimentares é na Growth!.html"
pasta_saida = "secoes"
os.makedirs(pasta_saida, exist_ok=True)

with open(arquivo_html, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

# Guia da árvore: extraia seções principais identificadas
secoes = [
    ("header.html", soup.find("header")),
    ("menuBar.html", soup.find(id="menuBar")),
    ("homeBannerPrincipal.html", soup.find(id="homeBannerPrincipal")),
    ("pitchbarHome.html", soup.find(id="pitchbarHome")),
    ("vitrine-home-black-kit.html", soup.select_one(".vitrine-home-black-kit")),
    ("bannersDuplos.html", soup.select_one(".bannersDuplos")),
    ("vitrine-home-black-outlet.html", soup.select_one(".vitrine-home-black-outlet")),
    ("vitrineTop20.html", soup.select_one(".vitrineTop20")),
    ("tabs-moda-acessorios.html", soup.select_one(".tabs-moda-acessorios")),
    ("bannerEbit.html", soup.select_one(".bannerEbit")),
    ("supCategoria.html", soup.select_one(".supCategoria")),
    ("vitrineHome2.html", soup.find(id="vitrineHome2")),
    ("depoimentosHome.html", soup.select_one(".depoimentosHome")),
    ("vitrineHome3.html", soup.find(id="vitrineHome3")),
    ("bannersBig.html", soup.select_one(".bannersBig")),
    ("bannersEsporte.html", soup.find(id="escolha-por-esportes")),
    ("bannerRodape.html", soup.select_one(".bannerRodape")),
    ("newsletter__container.html", soup.find(id="newsletter__container")),
    ("selosFinal.html", soup.select_one(".selosFinal")),
    ("topoRodape.html", soup.select_one(".topoRodape")),
    ("menuRodape.html", soup.find(id="menuRodape")),
    ("formasPag.html", soup.select_one(".formasPag")),
    ("infosRodape.html", soup.select_one(".infosRodape")),
    ("finalRodape.html", soup.select_one(".finalRodape")),
    ("uappiIcon.html", soup.select_one(".uappiIcon"))
]

for nome, elemento in secoes:
    if elemento:
        with open(os.path.join(pasta_saida, nome), "w", encoding="utf-8") as out:
            out.write(str(elemento))

print("Divisão concluída. Cada arquivo é legível individualmente.")