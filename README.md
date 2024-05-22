Pour exécuter le programme, il faut un service Linux ou Mac et le lancer dans un environnement virtuel.
Les fichiers de sauvegarde seront générés dans le dossier où se situe le fichier du programme. Essayez d'isoler ce fichier dans un dossier seul.

Exécutez ces commandes dans l'invité de commande pour commencer

- apt install python3
- apt install mysql-server
- pip install mysql-connector-python

Et voilà vous pouvez l'utiliser !


Si jamais vous avez un problème d'autorisation d'accès avec l'utilisateur root à la fonction creer_base_utilisateur()
changer le mot de passe à la ligne 127 et exécutez ces commandes

- ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';
- FLUSH PRIVILEGES;
- sudo service mysql restart

Si il y a d'autres problèmes, un environnement virtuel peut vous aider
Dirigez vous vers le dossier où est le fichier du programme puis exécutez ces commandes
- apt install python3.10-venv
- python3 -m venv venv
- source venv/bin/activate
