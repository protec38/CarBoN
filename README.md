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
CarBoN peut être utilisé en production en utilisant Docker, à l'aide du `docker-compose.yaml` fourni.

Il faut au préalable modifier le fichier `.env` pour fournir les informations de configuration. 

* `DJANGO_SETTINGS_MODULE`: par défaut à `settings.prod` pour utiliser la configuration de production (DEBUG désactivé)
* `DJANGO_DATABASE_ENGINE`: voir [https://docs.djangoproject.com/en/5.0/ref/settings/#engine]
* `DJANGO_DATABASE_HOST`: voir [https://docs.djangoproject.com/en/5.0/ref/settings/#host]
* `DJANGO_DATABASE_PORT`: voir [https://docs.djangoproject.com/en/5.0/ref/settings/#port]
* `DJANGO_DATABASE_NAME`: voir [https://docs.djangoproject.com/en/5.0/ref/settings/#name]
* `DJANGO_DATABASE_USER`: voir [https://docs.djangoproject.com/en/5.0/ref/settings/#user]
* `DJANGO_DATABSE_PASSWORD`: voir [https://docs.djangoproject.com/en/5.0/ref/settings/#password]

Le `docker-compose` par défaut fournit une image pour CarBoN à proprement parler, et une image nginx qui sert de reverse-proxy et sert les fichiers statiques.