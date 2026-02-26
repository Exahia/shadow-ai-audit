# Détection du Shadow AI — Signaux d'Alerte

Le Shadow AI est souvent invisible pour la DSI. Voici les signaux qui indiquent une utilisation non contrôlée d'IA dans votre organisation.

## Instructions
Pour chaque signal, évaluez : 🚨 Détecté | ⚠️ Suspecté | ✅ Absent

---

## Signaux réseau

- [ ] Trafic vers openai.com, chat.openai.com depuis le réseau entreprise
- [ ] Trafic vers gemini.google.com, claude.ai, copilot.microsoft.com
- [ ] Trafic vers des APIs IA tierces (api.openai.com, api.anthropic.com)
- [ ] Augmentation inexpliquée de la bande passante sortante

## Signaux comportementaux

- [ ] Employés copiant/collant de longs textes dans un navigateur
- [ ] Productivité soudainement accrue dans certains départements (sans outil officiel)
- [ ] Demandes récurrentes pour "accéder à ChatGPT" ou "avoir un outil IA"
- [ ] Abonnements personnels à des outils IA (notes de frais, remboursements)

## Signaux organisationnels

- [ ] Absence de politique d'usage IA formalisée
- [ ] Pas de solution IA approuvée disponible pour les employés
- [ ] Formations IA informelles entre collègues
- [ ] Documents/emails avec une qualité rédactionnelle soudainement meilleure

---

## Actions selon le score

| Signaux détectés | Action |
|-----------------|--------|
| 0-3 🚨 | Surveillance — mettre en place un monitoring |
| 4-7 🚨 | Alerte — audit formel recommandé |
| 8+ 🚨 | Urgence — Shadow AI généralisé, action immédiate |

## Prochaine étape

Utilisez le [questionnaire DSI](../questionnaire/questionnaire-dsi.md) pour quantifier précisément l'ampleur du Shadow AI.
