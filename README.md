# 🔍 Shadow AI Audit — Audit du Shadow AI en Entreprise

> Méthodologie, checklists et questionnaires pour auditer et quantifier les risques du Shadow AI dans votre organisation.

[![Made in France](https://img.shields.io/badge/Made%20in-France-blue)](https://exahia.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![RGPD](https://img.shields.io/badge/RGPD-Compliant-green)](https://exahia.com)

---

## Qu'est-ce que le Shadow AI ?

Le **Shadow AI** désigne l'utilisation non autorisée d'outils d'intelligence artificielle par les employés d'une organisation, sans validation de la DSI, du RSSI ou du DPO.

### L'ampleur du problème en 2026

- **49% des employés** utilisent des outils IA non sanctionnés par leur employeur
- **87% des cabinets juridiques** ont des collaborateurs utilisant des IA non autorisées sur des données sensibles
- **3 RSSI sur 4** ont découvert de l'IA générative non autorisée dans leur SI
- **4,63M€** : coût moyen d'une brèche de données dans les organisations à Shadow AI élevé
- **223 violations** de politique de données par mois en moyenne impliquant l'IA générative
- **32%** des exfiltrations de données d'entreprise passent par l'IA générative (canal n°1)
- **225 000+ identifiants ChatGPT** en vente sur le dark web

### Risques concrets

| Risque | Impact | Probabilité |
|--------|--------|-------------|
| Fuite de données clients/patients | Amende RGPD (jusqu'à 35M€ / 7% CA) | Élevée |
| Violation du secret professionnel | Sanctions ordinales, perte de licence | Élevée |
| Exposition Cloud Act | Saisie de données par autorités US | Moyenne |
| Perte de propriété intellectuelle | Brevets compromis, avantage concurrentiel | Moyenne |
| Non-conformité EU AI Act (août 2026) | Amendes 15-35M€ / 3-7% CA | Croissante |

## Méthodologie d'Audit en 3 Étapes

### Étape 1 : Cartographie (Semaine 1)
- Inventaire des outils IA utilisés (autorisés et non autorisés)
- Questionnaire anonyme aux employés (voir `questionnaire/`)
- Analyse des logs réseau (domaines IA contactés)
- Identification des données sensibles exposées

### Étape 2 : Évaluation des Risques (Semaine 2)
- Score de risque par département (voir `checklist/`)
- Matrice impact × probabilité
- Cartographie des flux de données vers les services IA
- Évaluation de la conformité RGPD et Cloud Act

### Étape 3 : Plan de Remédiation (Semaine 3)
- Recommandations priorisées (quick wins + actions structurantes)
- Proposition d'alternatives souveraines
- Politique d'usage IA à formaliser
- Planning de déploiement

## Contenu du Repo

```
shadow-ai-audit/
├── README.md
├── checklist/
│   ├── RGPD.md              # Checklist conformité RGPD × IA
│   ├── CLOUD-ACT.md         # Évaluation exposition Cloud Act
│   └── SHADOW-AI.md         # Détection Shadow AI (signaux, méthodes)
├── questionnaire/
│   ├── questionnaire-dsi.md # Questionnaire pour DSI/RSSI
│   └── exemple-reponses.json
├── tools/
│   └── score_audit.py       # CLI de scoring (JSON -> score + rapport)
└── rapport/
    └── template-rapport.md  # Template de rapport d'audit
```

## Quick Start (scoring automatique)

### 1) Générer un template de réponses

```bash
python3 tools/score_audit.py --init-template
```

Cela crée `questionnaire/reponses-template.json`.

### 2) Remplir le fichier de réponses

Valeurs attendues pour chaque question:
- `yes`
- `partial`
- `no`
- `na`

Vous pouvez partir de `questionnaire/exemple-reponses.json`.

### 3) Calculer le score de risque

```bash
python3 tools/score_audit.py \
  --responses questionnaire/exemple-reponses.json \
  --output-json rapport/score-summary.json \
  --output-md rapport/score-summary.md \
  --output-html rapport/score-summary.html

```

Le script calcule:
- un score global de risque (`0-100`)
- un score par domaine (`rgpd`, `cloud_act`, `shadow_ai`)
- une liste de priorités de remédiation
- un export HTML autonome lisible dans n'importe quel navigateur (`--output-html`)

## Checklists Disponibles

| Checklist | Audience | Questions |
|-----------|----------|-----------|
| [RGPD × IA](checklist/RGPD.md) | DPO, Juridique | 15 points de contrôle |
| [Cloud Act](checklist/CLOUD-ACT.md) | RSSI, DSI | 10 points de contrôle |
| [Shadow AI](checklist/SHADOW-AI.md) | DSI, RSSI, DPO | 12 signaux d'alerte |

## Pour qui ?

- **DSI** — Reprendre le contrôle des outils IA dans l'entreprise
- **RSSI** — Quantifier les risques de sécurité liés au Shadow AI
- **DPO** — Vérifier la conformité RGPD des usages IA
- **Dirigeants** — Comprendre l'exposition de l'entreprise

## Contexte Réglementaire

### RGPD (en vigueur)
- 2,3 milliards d'euros d'amendes en 2025 (+38%)
- 443 notifications de brèche par jour en Europe
- Article 28 : obligations du sous-traitant (= fournisseur IA)

### EU AI Act (application complète : 2 août 2026)
- Pénalités jusqu'à 35M€ ou 7% du CA mondial
- Obligations pour les systèmes IA à haut risque
- Documentation et traçabilité obligatoires

### Cloud Act (permanent)
- Donne au gouvernement US accès aux données des entreprises américaines
- S'applique même si les données sont stockées en Europe
- Conflit direct avec RGPD Article 48

## Lié à

Ce projet est développé par [Exahia](https://exahia.com), infrastructure IA souveraine B2B. L'audit Shadow AI est souvent la première étape avant le déploiement d'une solution souveraine.

## Licence

MIT — voir [LICENSE](LICENSE)
