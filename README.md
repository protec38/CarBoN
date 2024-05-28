# Installation
```bash
    pipenv install
    python manage.py migrate
```

# Données par défaut
Pour charger les données par défaut dans la base de données, exécuter la commande suivante :
```bash
    python manage.py loaddata main/fixtures/main/initial_data.json
```

**Ces données par défaut ne doivent pas être utilisées en production.**

## Utilisateurs par défaut
- **Super-utilisateur**
  - Username: admin
  - Password: admin
- **Utilisateur par défaut**
  - Username: user
  - Password: user

## Serveur de test
Pour lancer le serveur de test, exécuter la commande suivante :
```bash
    python manage.py runserver
```

Le serveur de test est accessible à l'adresse suivante : [http://127.0.0.1:8000/]()