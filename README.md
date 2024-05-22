Pour exécuter le programme, il faut un service Linux ou Mac et le lancer dans un environnement virtuel.
Les fichiers de sauvegarde seront générés dans le dossier où se situe le fichier du programme. Essayez d'isoler ce fichier dans un dossier seul.

- apt install python3
- apt install mysql-server
- pip install mysql-connector-python
- apt install python3.10-venv

Dirigez vous vers le dossier où est le fichier du programme
python3 -m venv venv
source venv/bin/activate

Et voilà vous pouvez l'utiliser !


Si jamais vous avez un problème d'autorisation d'accès avec l'utilisateur root à la fonction creer_base_utilisateur()
changer le mot de passe à la ligne 127 et exécutez ses commandes

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';
FLUSH PRIVILEGES;
sudo service mysql restart
