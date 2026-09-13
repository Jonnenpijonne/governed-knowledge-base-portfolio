---
type: decision
status: approved
date: 2026-09-13
classification: public-demo
owner_role: decision-owner
description: Päätös yhden auktoritatiivisen kodin periaatteesta.
---

# ADR-001: One authoritative home per information type

## Context

Sama tieto voi näkyä useassa käyttöliittymässä. Ilman nimettyä auktoritatiivista kotia
kopiot alkavat kilpailla keskenään ja muutosten jäljitettävyys heikkenee.

## Decision

Jokaiselle tietotyypille nimetään yksi auktoritatiivinen koti. Muut järjestelmät voivat
esittää, indeksoida tai välimuistittaa tiedon, mutta ne eivät saa hiljaisesti muuttua
masteriksi.

## Consequences

- ristiriidat voidaan ratkaista ennalta sovitulla säännöllä
- integraatiot pysyvät korvattavina
- hakukerros voidaan rakentaa uudelleen
- omistajuus on dokumentoitava tietotyypeittäin

