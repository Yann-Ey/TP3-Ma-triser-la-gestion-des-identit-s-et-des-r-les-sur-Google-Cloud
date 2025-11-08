Compte-rendu : TP Gestion des Identités et des Accès (IAM) sur Google CloudAuteur : Yann EyheregarayProjet : tp3-projetCe document résume les étapes, les commandes, les sorties et les conclusions des 8 exercices du Travail Pratique sur la gestion des identités, des accès, des rôles, et de l'audit sur Google Cloud Platform.🧾 Exercice 1 : Créer les identités de base1. Création du projetCommande :gcloud projects create tp3-projet
Explication :La commande gcloud projects create crée un nouveau projet avec l'identifiant unique tp3-projet.Sortie :Create in progress for [[https://cloudresourcemanager.googleapis.com/v1/projects/tp3-projet](https://cloudresourcemanager.googleapis.com/v1/projects/tp3-projet)].
Waiting for [operations/create_project.global.5762750760424319222] to finish...done.
Enabling service [cloudapis.googleapis.com] on project [tp3-projet]...
Operation "operations/acat.p2-1017833771517-842c591a-0ff7-4d17-89e1-223581cb452d" finished successfully.
2. Définition du projet actifCommande :gcloud config set project tp3-projet
Explication :Cette commande modifie la configuration locale du Cloud SDK afin d'éviter d'avoir à spécifier --project=tp3-projet à chaque commande.Sortie :Updated property [core/project].
3. Ajout des utilisateurs IAMa. Utilisateur Lecteur (Viewer)Objectif : Ajouter un utilisateur avec le rôle roles/viewer, pour un accès en lecture seule.Commande :gcloud projects add-iam-policy-binding tp3-projet --member="user:Yann.Eyheregaray@gmail.com" --role="roles/viewer"
b. Utilisateur Collaborateur (Editor)Objectif : Ajouter un second utilisateur avec le rôle roles/editor, pour un accès en lecture et écriture.Commande :gcloud projects add-iam-policy-binding tp3-projet --member="user:yannmc.anime@gmail.com" --role="roles/editor"
Résultat (Politique IAM mise à jour) :Updated IAM policy for project [tp3-projet].
bindings:
- members:
  - user:yannmc.anime@gmail.com
  role: roles/editor
- members:
  - user:eyheregaray.yann@gmail.com
  role: roles/owner
- members:
  - user:Yann.Eyheregaray@gmail.com
  role: roles/viewer
etag: BwZC6rj6ucI=
version: 1
4. Création d'un compte de serviceObjectif : Créer une identité non-humaine pour une future application backend.Commande :gcloud iam service-accounts create app-backend --display-name="Application Backend"
Sortie :Created service account [app-backend].
5. Vérification des comptes de serviceCommande :gcloud iam service-accounts list
Sortie :DISPLAY NAME         EMAIL                                           DISABLED
Application Backend  app-backend@tp3-projet.iam.gserviceaccount.com  False
🧾 Exercice 2 : Explorer IAM et les rôles1. Lister les membres IAMCommande :gcloud projects get-iam-policy tp3-projet --format="yaml"
Sortie (Politique IAM du projet) :bindings:
- members:
  - user:yannmc.anime@gmail.com
  role: roles/editor
- members:
  - user:eyheregaray.yann@gmail.com
  role: roles/owner
- members:
  - user:Yann.Eyheregaray@gmail.com
  role: roles/viewer
etag: BwZC6rj6ucI=
version: 1
Analyse :Le compte eyheregaray.yann@gmail.com est bien roles/owner (Propriétaire).Les rôles roles/viewer et roles/editor sont correctement attribués aux utilisateurs ajoutés.Les champs etag et version servent à gérer les modifications concurrentielles de la politique IAM.🧾 Exercice 3 : Portée des rôles et permissions atomiques1. Comprendre les permissions d’un rôleCommande :gcloud iam roles describe roles/storage.objectViewer
Sortie (partielle) :description: Grants access to view objects and their metadata, excluding ACLs. Can
  also list the objects in a bucket.
etag: AA==
includedPermissions:
- resourcemanager.projects.get
- resourcemanager.projects.list
- storage.folders.get
- storage.folders.list
- storage.managedFolders.get
- storage.managedFolders.list
- storage.objects.get
- storage.objects.list
name: roles/storage.objectViewer
stage: GA
title: Storage Object Viewer
2. Créer une ressource pour vos testsCommande :gcloud storage buckets create gs://bucket-tp3-projet-test
gcloud storage buckets create gs://bucket-tp3-projet-test-2
Sortie :Creating gs://bucket-tp3-projet-test/...
Creating gs://bucket-tp3-projet-test-2/...
3. Lister les permissions disponibles sur une ressourceQuelle commande ?gcloud iam list-testable-permissions //[storage.googleapis.com/projects/_/buckets/bucket-tp3-projet-test](https://storage.googleapis.com/projects/_/buckets/bucket-tp3-projet-test)
Identifiez celles qui permettent la lecture des objets :storage.objects.get (Titre : Read GCS Object Data and Metadata)storage.objects.list (Titre : List GCS Objects)4. Accorder un rôle sur une ressource spécifiqueQuelle commande ?gcloud storage buckets add-iam-policy-binding [URL-DU-BUCKET] --member="user:[EMAIL]" --role="[NOM-DU-ROLE]"Application (sur le "Lecteur") :gcloud storage buckets add-iam-policy-binding gs://bucket-tp3-projet-test --member="user:Yann.Eyheregaray@gmail.com" --role="roles/storage.objectViewer"
Sortie (Politique IAM du bucket) :bindings:
- members:
  - projectEditor:tp3-projet
  - projectOwner:tp3-projet
  role: roles/storage.legacyBucketOwner
- members:
  - projectViewer:tp3-projet
  role: roles/storage.legacyBucketReader
- members:
  - user:Yann.Eyheregaray@gmail.com
  role: roles/storage.objectViewer
etag: CAI=
kind: storage#policy
resourceId: projects/_/buckets/bucket-tp3-projet-test
version: 1
5. Tester l’accès restreint (Étape 5)Tests effectués en tant qu'utilisateur "Lecteur" (Yann.Eyheregaray@gmail.com).Commandes de test :# Test 1: Lister le contenu du bucket 1 (réussit, bucket vide)
PS C:\> gcloud storage ls gs://bucket-tp3-projet-test

# Test 2: Lister le contenu du bucket 2 (réussit, bucket vide)
PS C:\> gcloud storage ls gs://bucket-tp3-projet-test-2

# Test 3: Lister tous les buckets (réussit)
PS C:\> gcloud storage buckets list
---
...
name: bucket-tp3-projet-test
...
6. Étendre le rôle au niveau projet (Étape 6)Le même rôle est appliqué au niveau du projet entier.Quelle commande ? gcloud projects add-iam-policy-bindingApplication :gcloud projects add-iam-policy-binding tp3-projet --member="user:Yann.Eyheregaray@gmail.com" --role="roles/storage.objectViewer"
Sortie :Updated IAM policy for project [tp3-projet].
bindings:
- members:
  - user:yannmc.anime@gmail.com
  role: roles/editor
- members:
  - user:eyheregaray.yann@gmail.com
  role: roles/owner
- members:
  - user:Yann.Eyheregaray@gmail.com
  role: roles/storage.objectViewer
- members:
  - user:Yann.Eyheregaray@gmail.com
  role: roles/viewer
etag: BwZC7RvC9mc=
version: 1
7. Analyse fusionnée des Étapes 5 et 7La leçon la plus importante de cet exercice est la dangerosité des rôles de base (legacy).La comparaison entre la portée "Ressource" (Étape 4) et "Projet" (Étape 6) a été faussée car l'utilisateur "Lecteur" possédait le rôle roles/viewer au niveau du projet (attribué à l'Exercice 1).Ce rôle roles/viewer est si large qu'il inclut déjà la permission de lister le contenu de tous les buckets (storage.objects.list).Cela démontre que les rôles de base (Owner, Editor, Viewer) vont à l'encontre du principe de moindre privilège et ne devraient pas être utilisés en production. Ils accordent des milliers de permissions et rendent impossible la gestion fine des accès, comme nous l'avons constaté lorsque nos tests d'accès restreint (Étape 5) ont réussi alors qu'ils auraient dû échouer.8. Nettoyer la configurationQuelle commande ? remove-iam-policy-bindingApplication :# Retrait du rôle au niveau projet
gcloud projects remove-iam-policy-binding tp3-projet --member="user:Yann.Eyheregaray@gmail.com" --role="roles/storage.objectViewer"

# Retrait du rôle au niveau bucket
gcloud storage buckets remove-iam-policy-binding gs://bucket-tp3-projet-test --member="user:Yann.Eyheregaray@gmail.com" --role="roles/storage.objectViewer"
Sorties :# Sortie du retrait projet
Updated IAM policy for project [tp3-projet].
bindings:
- members:
  - user:yannmc.anime@gmail.com
  role: roles/editor
# ... (le rôle storage.objectViewer est bien parti)
# Sortie du retrait bucket
bindings:
# ... (le rôle storage.objectViewer est bien parti)
etag: CAM=
Analyse finale :Après avoir retiré les rôles storage.objectViewer, les tests d'accès au contenu des buckets réussissaient toujours. Cela confirme notre analyse : le rôle roles/viewer (Lecteur) au niveau du projet est un rôle legacy trop large qui accorde déjà cet accès.🧾 Exercice 4 : Créer un rôle personnalisé1. Identifier les permissions nécessairesDéployer un service ? run.services.create (initial) et run.services.update (mises à jour).Lister les services ? run.services.list (la liste) et run.services.get (les détails).Supprimer un service ? run.services.delete.2. Créer le fichier de définitionSections obligatoires ? title, description, stage, includedPermissions.Contenu du fichier role-cloudrun-deployer.yaml :title: "Déployeur Cloud Run Personnalisé"
description: "Permet de créer, lister, mettre à jour et supprimer des services Cloud Run."
stage: "GA"
includedPermissions:
  # Permissions pour créer et mettre à jour
  - run.services.create
  - run.services.update

  # Permissions pour lister et lire
  - run.services.list
  - run.services.get

  # Permission pour supprimer
  - run.services.delete

  # Permission essentielle pour le déploiement
  - iam.serviceAccounts.actAs
3. Créer le rôle dans votre projetQuelle commande ? gcloud iam roles createApplication :gcloud iam roles create deployeurCloudRun --project=tp3-projet --file=role-cloudrun-deployer.yaml
Sortie :WARNING: API is not enabled for permissions: [...]
Created role [deployeurCloudRun].
...
name: projects/tp3-projet/roles/deployeurCloudRun
...
Vérification :gcloud iam roles describe deployeurCloudRun --project=tp3-projet
4. Attribuer le rôle à un utilisateurQuelle commande ? gcloud projects add-iam-policy-bindingApplication :gcloud projects add-iam-policy-binding tp3-projet --member="user:yannmc.anime@gmail.com" --role="projects/tp3-projet/roles/deployeurCloudRun"
Sortie :Updated IAM policy for project [tp3-projet].
bindings:
- members:
  - user:yannmc.anime@gmail.com
  role: projects/tp3-projet/roles/deployeurCloudRun
# ... autres rôles
etag: BwZC7aIgZKE=
version: 1
Pourquoi tester avec un autre compte ?Mon compte principal (eyheregaray.yann@gmail.com) est Owner et a déjà toutes les permissions, ce qui fausserait le test. L'utilisation du compte "Collaborateur" permet un test isolé pour valider que le rôle personnalisé accorde exactement les permissions nécessaires.5. Tester le rôleTests effectués en tant que "Collaborateur" (yannmc.anime@gmail.com).Analyse de l'échec initial : Les premières tentatives ont échoué avec FAILED_PRECONDITION: UREQ_TOS_NOT_ACCEPTED. L'erreur n'était pas due au rôle, mais au fait que l'API Cloud Run n'avait jamais été activée. L'acceptation des conditions de service a dû être faite par le compte Owner.Résultats (après activation de l'API) :# Test 1: Lister (réussit)
PS C:\> gcloud run services list --region=europe-west9
Listed 0 items.

# Test 2: Déployer (réussit)
PS C:\> gcloud run deploy service-test-role --image=us-docker.pkg.dev/cloudrun/container/hello --region=europe-west9 --allow-unauthenticated
Service [service-test-role] revision [...] deployed.
Service URL: [https://service-test-role-1017833771517.europe-west9.run.app](https://service-test-role-1017833771517.europe-west9.run.app)

# Test 3: Supprimer (réussit)
PS C:\> gcloud run services delete service-test-role --region=europe-west9
Service [service-test-role] will be deleted.
Do you want to continue (Y/n)?  y
Deleting [service-test-role]...done.
Deleted service [service-test-role].
Conclusion : Après activation de l'API par l'Owner, les trois tests ont réussi. Cela valide que la liste des permissions dans le rôle personnalisé était correcte et suffisante.6. Analyser et corrigerAnalyse : L'erreur initiale (UREQ_TOS_NOT_ACCEPTED) n'était pas liée aux permissions du rôle, mais à la configuration du projet. Aucune correction du fichier YAML n'a été nécessaire.Commande de mise à jour (si nécessaire) : gcloud iam roles update [ROLE_ID] ...Action de correction : L'activation de l'API Cloud Run par le compte Owner a résolu le problème de précondition.7. Nettoyer la configurationQuelle commande ? gcloud iam roles deleteQuand l'utiliser ? Lorsqu'un rôle est temporaire, obsolète, ou pour réduire la surface d'attaque et maintenir une bonne hygiène de sécurité.🧾 Exercice 5 : Gérer les comptes de service1. Attribuer le rôle appropriéPermissions requises : storage.objects.list et storage.objects.get.Rôle prédéfini : roles/storage.objectViewer.Commande :gcloud storage buckets add-iam-policy-binding gs://bucket-tp3-projet-test --member="serviceAccount:app-backend@tp3-projet.iam.gserviceaccount.com" --role="roles/storage.objectViewer"
Sortie :bindings:
- members:
  - serviceAccount:app-backend@tp3-projet.iam.gserviceaccount.com
  role: roles/storage.objectViewer
...
Pourquoi au niveau du bucket ? Pour respecter le principe du moindre privilège. Si le rôle avait été appliqué au projet, l'application (si compromise) aurait pu lire tous les buckets.2. Préparer l’applicationBibliothèques : google-cloud-storage, Flask, et gunicorn (pour la production).Variable d'environnement : BUCKET_NAME (utilisée dans le code via os.environ.get).Authentification : L'application utilise les "Application Default Credentials" (ADC). En s'exécutant sur Cloud Run, elle adopte automatiquement l'identité du compte de service (app-backend) qui lui est attaché.3. Conteneuriser l’applicationDockerfile :# Étape 1 : Utiliser une image de base Python officielle et légère
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier le fichier des dépendances
COPY requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le reste du code de l'application (main.py)
COPY . .

# Étape 6 : Définir le port par défaut que Cloud Run écoutera
ENV PORT 8080

# Étape 7 : Commande pour exécuter l'application en production avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "main:app"]
Instruction de port : La variable d'environnement PORT (définie par ENV PORT 8080 et lue par Gunicorn) détermine le port d'écoute.Test local : docker build -t app-test . puis docker run -p 8080:8080 -e BUCKET_NAME=... app-test.Commande de publication : gcloud builds submit --tag [IMAGE_NAME] .4. Déployer sur Cloud RunLe déploiement s'est déroulé en trois commandes principales :1. Création du dépôt Artifact Registrygcloud artifacts repositories create cloudrun-repo --repository-format=docker --location=europe-west9
Sortie : Created repository [cloudrun-repo].2. Construction et Publication de l'imagegcloud builds submit --tag europe-west9-docker.pkg.dev/tp3-projet/cloudrun-repo/app-backend .
Sortie : STATUS: SUCCESS3. Déploiement du service sur Cloud Run(Note : La variable BUCKET_NAME a été corrigée de gs://... à ...)gcloud run deploy app-backend-service --image=europe-west9-docker.pkg.dev/tp3-projet/cloudrun-repo/app-backend --service-account=app-backend@tp3-projet.iam.gserviceaccount.com --region=europe-west9 --set-env-vars=BUCKET_NAME=bucket-tp3-projet-test --allow-unauthenticated
Option de compte de service : L'option --service-account a été utilisée pour attacher l'identité app-backend.Vérification console : L'identité est visible dans la console Cloud Run, sous l'onglet "Sécurité" du service.5. Tester le serviceTest 1 : Accès au bon bucket (Succès)Accès à .../list (avec BUCKET_NAME=bucket-tp3-projet-test).Résultat : [] (JSON vide), confirmant l'accès.Test 2 : Accès à un autre bucket (Échec)Le service a été redéployé avec BUCKET_NAME=bucket-tp3-projet-test-2.Résultat : Erreur 403 Forbidden (Accès refusé).Conclusion : Le test prouve que le compte de service app-backend n'a l'accès qu'au bucket test-1, conformément au principe de moindre privilège.6. Observer les logsActivation : Les logs "Data Access" pour Cloud Storage ont dû être activés manuellement.Identité (principalEmail) : app-backend@tp3-projet.iam.gserviceaccount.comConfirmation : Le log (voir capture) confirme que app-backend a exécuté la méthode storage.objects.list sur la ressource bucket-tp3-projet-test.7. Nettoyer la configurationCommande :gcloud run services delete app-backend-service --region=europe-west9
Risque des comptes inactifs/surdimensionnés : Un compte inactif est une "porte" oubliée. Un compte surdimensionné (ex: Editor) transforme une faille applicative mineure en une faille de sécurité majeure pour tout le projet.🧾 Exercice 6 : Délégation (Impersonation)1. Créer un nouveau compte de serviceCommande :gcloud iam service-accounts create deploy-automation --display-name="Compte de service pour automation"
2. Accorder la permission d'impersonationRôle requis : roles/iam.serviceAccountTokenCreator (Créateur de jetons de compte de service).Portée : Appliquée directement sur le compte de service deploy-automation.Risque (si appliqué au projet) : Permettrait à quiconque d'usurper l'identité de ce compte et d'escalader ses propres privilèges.Commande :gcloud iam service-accounts add-iam-policy-binding deploy-automation@tp3-projet.iam.gserviceaccount.com --member="user:eyheregaray.yann@gmail.com" --role="roles/iam.serviceAccountTokenCreator"
Sortie :Updated IAM policy for serviceAccount [deploy-automation@tp3-projet.iam.gserviceaccount.com].
bindings:
- members:
  - user:eyheregaray.yann@gmail.com
  role: roles/iam.serviceAccountTokenCreator
etag: BwZC_ilqTpg=
version: 1
3. Tester l’impersonationOption CLI : --impersonate-service-accountCommande de test :gcloud storage buckets list --impersonate-service-account="deploy-automation@tp3-projet.iam.gserviceaccount.com"
Résultat :WARNING: This command is using service account impersonation...
ERROR: (gcloud.storage.buckets.list) HTTPError 403: deploy-automation@tp3-projet.iam.gserviceaccount.com does not have storage.buckets.list access...
Analyse : L'erreur 403 est un succès de test. Elle prouve que :L'impersonation a réussi (la commande a été exécutée en tant que deploy-automation).Le compte deploy-automation lui-même n'a aucune permission (ce qui est correct).4. Cas d'usage et bonnes pratiquesCas d'usage : Un pipeline CI/CD (GitHub Actions, GitLab) qui s'authentifie avec une identité faible, puis impersonate un compte de service deploy-automation pour obtenir un jeton temporaire de déploiement, sans jamais stocker de clé privée.Bonnes pratiques : Principe du moindre privilège (ne donner que roles/run.admin au SA), portée limitée (donner TokenCreator à une seule identité), audit.5. Observer dans les logsCompte impersoné : protoPayload.authenticationInfo.principalEmail (ex: deploy-automation@...).Utilisateur délégant : protoPayload.authenticationInfo.firstPartyPrincipal (ex: eyheregaray.yann@gmail.com).Traçabilité : Le log enregistre les deux identités, assurant une traçabilité complète.6. Nettoyer la configurationCommande :gcloud iam service-accounts remove-iam-policy-binding deploy-automation@tp3-projet.iam.gserviceaccount.com --member="user:eyheregaray.yann@gmail.com" --role="roles/iam.serviceAccountTokenCreator"
🧾 Exercice 7 : Accès temporaire via IAM Conditions1. Identifier le cas d'usageRôle choisi : roles/run.admin (Administrateur Cloud Run) pour une élévation de privilège temporaire.2. Définir la condition temporelleSyntaxe CEL : request.time < timestamp("YYYY-MM-DDTHH:MM:SSZ")Condition utilisée : request.time < timestamp("2025-11-07T10:40:00Z") (11:40 CET)3. Créer le rôle conditionnelCommande :gcloud projects add-iam-policy-binding tp3-projet `
    --member="user:yannmc.anime@gmail.com" `
    --role="roles/run.admin" `
    --condition="expression=request.time < timestamp('2025-11-07T10:40:00Z'),title=acces_temporaire_run,description=Acces admin temporaire"
Vérification console : Une icône d'horloge ⏰ apparaît à côté du rôle dans la console IAM.4. Tester l'accès (Avant et Après expiration)Test AVANT expiration (11:30 CET) :gcloud run services list --region=europe-west9 ➔ SUCCÈS (Listed 0 items.).Le rôle était actif.Test APRÈS expiration (le lendemain) :gcloud run services list --region=europe-west9 ➔ SUCCÈS (Listed 0 items.).5. Conclusion de l'Exercice 7Le test d'expiration a échoué à échouer, pour la même raison que l'Exercice 3 : le rôle roles/editor (Éditeur) permanent du collaborateur.Bien que le rôle conditionnel roles/run.admin ait correctly expiré, la permission run.services.list était toujours accordée par le rôle Editor (legacy).Cela démontre une fois de plus que les rôles de base (legacy) sont trop larges et vont à l'encontre du principe de moindre privilège. Ils rendent inefficaces les contrôles de sécurité granulaires, tels que les conditions temporelles.6. Nettoyer la configurationCommande :gcloud projects remove-iam-policy-binding tp3-projet --member="user:yannmc.anime@gmail.com" --role="roles/run.admin" --all
🧾 Exercice 8 : Auditer les accès1. Différence entre les types de logsAdmin Activity (Activé par défaut) : Modifie la configuration (ex: SetIamPolicy).Data Access (Désactivé par défaut) : Lit ou écrit des données (ex: storage.objects.list).2. Observer les changements IAM (SetIamPolicy)En réglant la plage de temps sur "7 derniers jours", les logs de modification IAM ont été trouvés.Log JSON (Exemple) :{
  "insertId": "-ahoc15e10q0o",
  "logName": "projects/tp3-projet/logs/cloudaudit.googleapis.com%2Factivity",
  "protoPayload": {
    "@type": "[type.googleapis.com/google.cloud.audit.AuditLog](https://type.googleapis.com/google.cloud.audit.AuditLog)",
    "authenticationInfo": {
      "principalEmail": "eyheregaray.yann@gmail.com"
    },
    "methodName": "SetIamPolicy",
    "resourceName": "projects/tp3-projet",
    "serviceName": "cloudresourcemanager.googleapis.com",
    "status": {}
  },
  "timestamp": "2025-11-06T10:42:32.760008Z"
}
Analyse :Initiateur : principalEmail: "eyheregaray.yann@gmail.com"Ressource : resourceName: "projects/tp3-projet"Résultat : status: {} (Succès)3. Analyser les accès Cloud Run (Data Access)Le log de l'Exercice 5 (que nous avions activé manuellement) a été retrouvé.Log JSON (Exemple) :{
  "logName": "projects/tp3-projet/logs/cloudaudit.googleapis.com%2Fdata_access",
  "protoPayload": {
    "authenticationInfo": {
      "principalEmail": "app-backend@tp3-projet.iam.gserviceaccount.com"
    },
    "methodName": "storage.objects.list",
    "resourceName": "projects/_/buckets/bucket-tp3-projet-test",
    "status": {}
  },
  "timestamp": "2025-11-07T09:42:17.924973117Z"
}
Analyse :Opération : methodName: "storage.objects.list"Identité : principalEmail: "app-backend@tp3-projet.iam.gserviceaccount.com" (prouvant l'accès par le compte de service).4. Exporter les logsOption : "Collecteurs de logs" (Log Sinks) dans Cloud Logging.Objectif : Exporter vers BigQuery (pour analyse) ou Cloud Storage (pour conservation longue durée) à des fins de conformité et de sécurité.Format : LogEntry (JSON), avec les champs clés timestamp, resource, et protoPayload.5. Créer une alerteMéthode : Créer une "Alerte basée sur les journaux" (Log-based Alert) depuis l'Explorateur de journaux.Événement : Un filtre sur protoPayload.methodName="SetIamPolicy" déclencherait une alerte à chaque fois qu'une politique IAM est modifiée.Notification : Via Email, Slack, PagerDuty, SMS, etc.6. Consigner les observations (Log d'audit final)L'exemple de log SetIamPolicy de l'étape 2 (ci-dessus) sert d'enregistrement parfait :Compte initiateur : protoPayload.authenticationInfo.principalEmail: "eyheregaray.yann@gmail.com"Ressource modifiée : protoPayload.resourceName: "projects/tp3-projet"Date et heure : timestamp: "2025-11-06T10:42:32.760008Z"Résultat : protoPayload.status: {} (Succès)Conclusion Générale du TPCe TP a couvert les piliers fondamentaux d'IAM. Les leçons les plus importantes sont :Le danger des rôles de base (Legacy) : Les rôles Owner, Editor, et Viewer sont trop permissifs pour un environnement de production. Ils rendent les contrôles granulaires (par portée ou condition) inefficaces, comme démontré aux Exercices 3 et 7.Le principe du moindre privilège : Les permissions doivent être accordées au niveau le plus bas (la ressource, ex: le bucket) plutôt qu'au niveau projet (démontré à l'Exercice 5).La sécurité des comptes de service : L'impersonation (Exercice 6) est largement supérieure à l'utilisation de clés JSON, car elle est temporaire et traçable.L'audit est essentiel : Les logs "Admin Activity" et "Data Access" (Exercice 8) sont la seule source de vérité pour savoir "qui a fait quoi et quand".
