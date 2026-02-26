# Évaluation Exposition Cloud Act

Le Cloud Act (Clarifying Lawful Overseas Use of Data Act, 2018) permet au gouvernement américain d'exiger l'accès aux données détenues par des entreprises américaines, **quel que soit le lieu de stockage**.

## Instructions
Pour chaque point, évaluez votre exposition : 🔴 Exposé | 🟡 Partiel | 🟢 Protégé

---

## 1. Fournisseurs IA

- [ ] Utilisez-vous ChatGPT / OpenAI ? → 🔴 Entreprise US, soumise au Cloud Act
- [ ] Utilisez-vous Microsoft Copilot / Azure OpenAI ? → 🔴 Entreprise US
- [ ] Utilisez-vous Google Gemini / Vertex AI ? → 🔴 Entreprise US
- [ ] Utilisez-vous Amazon Bedrock ? → 🔴 Entreprise US

## 2. Infrastructure cloud

- [ ] Vos données IA sont-elles hébergées chez un fournisseur US (AWS, Azure, GCP) ? → 🔴
- [ ] Votre fournisseur cloud a-t-il une filiale américaine ? → 🟡
- [ ] Utilisez-vous un hébergeur souverain européen (OVHcloud, Scaleway, etc.) ? → 🟢

## 3. Données concernées

- [ ] Des données personnelles (PII) sont-elles envoyées à des services IA US ?
- [ ] Des données de santé (Art. 9 RGPD) transitent-elles par des services US ?
- [ ] Des données couvertes par le secret professionnel sont-elles exposées ?

## 4. Mesures de protection

- [ ] Un DPA (Data Processing Agreement) existe-t-il avec vos fournisseurs IA ?
- [ ] Les clauses contractuelles types (CCT) sont-elles en place ?
- [ ] Un chiffrement end-to-end est-il actif (clés non détenues par le fournisseur US) ?

---

## Score d'exposition

| Résultat | Niveau de risque |
|----------|-----------------|
| 0-2 🔴 | Faible — exposition limitée |
| 3-5 🔴 | Modéré — actions recommandées |
| 6+ 🔴 | Élevé — migration urgente vers solution souveraine |
