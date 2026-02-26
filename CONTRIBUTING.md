# Contribuer à Shadow AI Audit

Merci de votre intérêt pour ce projet. Les contributions sont les bienvenues.

## Comment contribuer

### Signaler une erreur ou une amélioration
Ouvrez une issue sur GitHub avec :
- Une description claire du problème ou de l'amélioration
- Le fichier concerné
- Si possible, une proposition de correction

### Proposer une modification
1. Forkez le repo
2. Créez une branche (`git checkout -b amelioration/ma-contribution`)
3. Commitez vos modifications (`git commit -m "Ajoute: [description]"`)
4. Poussez votre branche (`git push origin amelioration/ma-contribution`)
5. Ouvrez une Pull Request

## Types de contributions acceptées

- Mise à jour des statistiques et chiffres
- Ajout de nouveaux signaux Shadow AI
- Amélioration des checklists existantes
- Nouvelles checklists (ex : NIS2, DORA, ISO 27001 × IA)
- Traductions (EN, DE, ES, IT)
- Corrections de formulations ou de fautes

## Standards

- Markdown propre et bien formaté
- Sources citées pour les statistiques
- Langage professionnel, adapté DSI/RSSI/DPO
- Pas de contenu promotionnel abusif

## Validation locale

Pour valider les changements sur l'outil de scoring :

```bash
python3 tools/score_audit.py \
  --responses questionnaire/exemple-reponses.json \
  --output-json /tmp/score-summary.json \
  --output-md /tmp/score-summary.md
```

## Contact

Pour toute question : [hello@exahia.com](mailto:hello@exahia.com) ou via une issue GitHub.
