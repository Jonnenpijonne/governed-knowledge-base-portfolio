---
type: architecture
status: approved
date: 2026-09-13
classification: public-demo
owner_role: information-owner
description: Auktoritatiivisten lähteiden ja yhteisen hakukerroksen vastuurajat.
---

# Source boundaries

## Päätavoite

Tieto voidaan jakaa useaan järjestelmään, kun jokaiselle tietotyypille on yksi
auktoritatiivinen koti ja yhteinen hakukerros säilyy johdettuna näkymänä.

| Tietotyyppi | Auktoritatiivinen koti | Esimerkki | Ei kuulu tänne |
|---|---|---|---|
| Operatiivinen tila | työjonojärjestelmä | tehtävä, tila, omistaja | pysyvä ohje |
| Pysyvä dokumentti | dokumenttivarasto | raportti, sopimus, käyttöohje | tehtävän hetkellinen tila |
| Sääntö ja päätös | Git-repo | arkkitehtuuriperiaate, ADR | henkilötieto tai asiakasdata |
| Haku ja analyysi | johdettu hakukerros | yhdistetty löydettävyys | master-data |

## Ingressin vähimmäisehdot

1. Lähde luetaan vain hyväksytystä haarasta.
2. Include/exclude-rajaukset määritellään ennen ensimmäistä ajoa.
3. Tunnuksella on vain sisältöjen lukuoikeus rajattuun repoon.
4. Tuntemattomia tiedostotyyppejä ei käsitellä oletuksena.
5. Indeksi voidaan rakentaa uudelleen auktoritatiivisista lähteistä.

