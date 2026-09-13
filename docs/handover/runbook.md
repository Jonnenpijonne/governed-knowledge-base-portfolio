---
type: runbook
status: approved
date: 2026-09-13
classification: public-demo
owner_role: technical-owner
description: Tietopohjan validointi-, julkaisu- ja palautusohje.
---

# Handover runbook

## Normaali muutos

1. Tee rajattu muutos omassa haarassa.
2. Aja `python scripts/validate.py`.
3. Aja `python -m unittest discover -s tests -p 'test_*.py'`.
4. Avaa pull request ja kuvaa tavoite, rajaus, riskit ja todennus.
5. Toinen henkilö katselmoi ennen yhdistämistä `main`-haaraan.

## Häiriötilanne

Jos validointi epäonnistuu, muutosta ei yhdistetä. Jos virhe havaitaan yhdistämisen
jälkeen, tee palautus uutena commitina tai revertinä. Älä kirjoita historiaa uusiksi.

## Omistajuus

- Päätösomistaja hyväksyy toimintaperiaatteet.
- Tekninen omistaja ylläpitää tarkistuksia ja työnkulkua.
- Vähintään toinen henkilö pystyy suorittamaan tämän runbookin.

## Julkiseksi avaamisen portti

Ennen mahdollista julkaisua tarkista koko git-historia, tiedostot, workflow-lokit,
repon asetukset ja lisenssi. Yksityisyysasetuksen muuttaminen ei korvaa sisältöauditointia.

