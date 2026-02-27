# Rapport de score Shadow AI

- Genere le: 2026-02-26T22:20:12.892803+00:00
- Score global: **65.0/100** (eleve)

## Scores par section

| Section | Score | Niveau |
|---|---:|---|
| rgpd | 55.0/100 | eleve |
| cloud_act | 60.0/100 | eleve |
| shadow_ai | 80.0/100 | critique |

## Priorites de remediation

| Section | Question | Reponse |
|---|---|---|
| rgpd | DPA en place | no |
| rgpd | Detection PII avant envoi LLM | no |
| rgpd | DPIA realise | no |
| cloud_act | Usage OpenAI/ChatGPT | yes |
| cloud_act | Fournisseur avec lien juridique US | yes |
| cloud_act | PII envoyee a des services US | yes |
| cloud_act | Chiffrement E2E avec cles client | no |
| shadow_ai | Trafic vers domaines IA publics | yes |
| shadow_ai | Appels API externes IA | yes |
| shadow_ai | Absence de politique IA | yes |

## Legend

- `0-24.9`: risque faible
- `25-49.9`: risque modere
- `50-74.9`: risque eleve
- `75-100`: risque critique
