---
type: decision
status: proposed
date: 2026-09-13
classification: public-demo
owner_role: decision-owner
description: Ehdotus rajatusta vain luku -ingressistä AI- ja hakukerrokseen.
---

# ADR-002: Read-only AI ingress

## Context

Hyväksytyt toimintamallidokumentit halutaan tehdä haettaviksi ilman, että hakukerros
saa kirjoitusoikeutta lähteeseen tai ingestoi koko repoa oletuksena.

## Proposed decision

Ensimmäinen versio lukee vain `main`-haaraa, sallittuja polkuja ja tunnettuja
tekstimuotoja. Palvelutunnukselle annetaan vain tähän repoon rajattu sisältöjen
lukuoikeus. Toteutus vaatii erillisen hyväksynnän; tämä ADR ei itsessään käynnistä
integraatiota.

## Acceptance criteria

- branch lock: `main`
- explicit include/exclude rules
- repository-scoped read permission
- allowlist: Markdown, plain text, CSV, YAML ja JSON
- audit log without document content

