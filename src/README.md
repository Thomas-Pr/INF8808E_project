Pour notre projet, nous avons choisi l'architecture suivante : 

- asset/
- app.py 
- server.py
- {nom de visualisation}.py  
- template.py
  
Dans le dossier asset, on va retrouver les data et les fonts utilisées.  
Dans le fichier app.py se trouve le code pour afficher les visualisations sur l'application Dash ainsi que la structure de la page web.  
Dans le fichier server.py, on retrouve le code pour lancer le server de l'application Dash.  
Dans le fichier template.py, on retrouve le template de certaines visualisations.  
Enfin, on retrouve dans les fichiers {nom de visualisation}.py, le code permettant de générer la visualisation correspondante.  

Pour lancer l'appli Dash, il suffit de run la commande suivante: 
python server.py

  
