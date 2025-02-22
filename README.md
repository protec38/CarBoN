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

# Installation en production
## Docker
CarBoN peut être utilisé en production en utilisant une image Docker, construite en utilisant le Dockerfile présent à la racine. 

L'image a besoin des variables d'environnement suivantes pour fonctionner :
* `DJANGO_SETTINGS_MODULE` : par défaut à `settings.prod` pour utiliser la configuration de production (DEBUG désactivé)
* `DJANGO_DATABASE_ENGINE` : voir [https://docs.djangoproject.com/en/5.0/ref/settings/#engine]
* `DJANGO_DATABASE_HOST` : voir [https://docs.djangoproject.com/en/5.0/ref/settings/#host]
* `DJANGO_DATABASE_PORT` : voir [https://docs.djangoproject.com/en/5.0/ref/settings/#port]
* `DJANGO_DATABASE_NAME` : voir [https://docs.djangoproject.com/en/5.0/ref/settings/#name]
* `DJANGO_DATABASE_USER` : voir [https://docs.djangoproject.com/en/5.0/ref/settings/#user]
* `DJANGO_DATABASE_PASSWORD` : voir [https://docs.djangoproject.com/en/5.0/ref/settings/#password]
* `DJANGO_SECRET_KEY` : voir ["https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-SECRET_KEY"]

Cette image ne sert pas les fichiers statiques : ils sont exposés dans le dossier /app/static et doivent être servis par un reverse proxy sur l'url /static

Le `docker-compose` fournit un example de configuration où l'on expose les différents dossiers requis. Le dossier app/data n'est utile que si Sqlite est utilisé comme moteur de base de donnée.  