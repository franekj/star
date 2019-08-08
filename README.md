# STAR - Řídící systém

Repozitory obsahuje kompletní balík Řídícího systému STAR, který se skládá z dockerových kontejnerů. 

Vlastní katalog CKAN a jeho pluginy se postaví pomocí **Dockerfile**. 
Ostatni obrazy kontejneru jsou použity hotové. 

## Systémové nároky

Pokud je **Řídící systém STAR** instalován kompletní, tedy včetně komponent Elasticsearch a Kibana, a předpokládá se jeho produkční nasazení,vyžaduje virtuální stroj v této konfiguraci:

- Platforma: **debian:stable** nebo **ubuntu:bionic**. 
- vCPU:  4-8
- vRAM:  nejméně 64GB
- vHDD:  1TB
- Kontejnerová platforma: **Docker** v19 nebo vyšší, **docker-compose**  v1.24 nebo vyšší
- Správa zdrojů:  git
- V kernelu nastavit **vm.max_map_count=262144** !!!

Na vitruální stroj s těmito parametry a touto předinstalací lze pak jednoduchým způsobem nasadit **STAR Řídící systém**:

## Nasazení

      cd project/ckan/contrib/docker/

Zde se nastaví systémové proměnné v souboru **.env** (lze použít předpřipravený .env.template) a pak se spustí setavení systému: 

      docker-compose build
      docker-compose up -d
 

 ## Úkony po nasazení

1. Nasazenou instanci systému zpřístupníme pomocí reverzní proxy tak, aby to odpovídalo naší bezpečnostní politice. 
2. Po nasazení zkontrolujeme, zda všechny kontejnery běží. Pokud ano, můžeme začít instanci systému používat
3. Pokud ne, použijeme vložený **Portainer** k prozkoumání logů a přípoadně upravíme konfiguraci jednotlivých kontejnerů. 
