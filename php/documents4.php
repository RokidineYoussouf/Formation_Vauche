<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-Script-Type" content="text/javascript" />
  <title>Outils informatiques</title>
  
  <link rel="stylesheet" type="text/css" media="screen,projection,print" href="images/setup.css" />
  <link rel="stylesheet" type="text/css" media="screen,projection,print" href="images/text.css" />
  <link rel="stylesheet" type="text/css" media="screen,projection,print" href="images/plan.css" />
  <link rel="icon" type="image/x-icon" href="images/favicon.ico" />

  <!-- Affichage de code
  <link rel="stylesheet" type="text/css" media="screen,projection,print" href="highlight.js/styles/googlecode.css" />
  <script src="highlight.js/highlight.pack.js"></script>
  <script>hljs.initHighlightingOnLoad();</script>
 -->
 
<hr>
<br /><a name="Docker"></a>
<center><h1>Docker</h1></center><ul><li><ul>
<li><b>Configuration de Docker</b>
<ol>
<li><i>Installation de Docker</i> : <br />
Créer un compte sur le <a href="https://hub.docker.com" target="dh">DockerHub</a>.<br />
Installer Docker en local.
</ol>
</li>
</ul></li><li><ul>
<li><b>Utilisation de Docker</b>
<ol start=2>
<li><i>Utiliser une première image Docker</i> : <br />
Récupérer l'image nommée <b>hello-world</b> sur le DockerHub et la lancer.
</li>
<li><i>Base de données</i> : <br />
Récupérer l'image d'une base de données <b>PostgreSQL</b>.<br />
La lancer et vous y connecter à partir du logiciel <b>pgadmin</b>.
</li>
</ol>
</li>
</ul></li><li><ul>
<li><b>Construire des images</b>
<ol start=4>
<li><i>Persistance des données</i> : <br />
Résoudre le problème de persistance des données de votre exercice précédent. <br />
Les données sont actuellement effacées lors de l'arrêt du conteneur.
</li>
<li><i>Créer une première image Docker</i> : <br />
Créer un <i>docker-compose</i> avec une base de données <b>MySQL</b> et un conteneur <b>WordPress</b>.
</li>
<li><i>Construire un serveur</i> : <br />
Créer un serveur PHP à partir d'un <i>Dockerfile</i>, l'image de base utilisée pour PHP sera <b>php:8.2-cli</b>.<br />
Une fois terminé, ajouter une base de données <b>MySQL</b> pour gérer un serveur <b>phpMyAdmin</b>.
</li>
</ol>
</li>
</ul></li></ul><hr>
 <br />
	
    </div><!-- main-content -->
    <!-- C. Bas de page -->      
    <div class="footer"><p>Copyright © 2024 &nbsp; Youssouf Roki-dine </p>

    </div><!-- footer -->      
  </div><!-- page_container -->
</body>
</html>