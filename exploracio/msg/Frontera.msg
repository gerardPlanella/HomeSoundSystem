int32 id 	# identificador de la frontera
uint32 size	# tamany de la frontera

geometry_msgs/Point centre_punt		# centre de la frontera
uint32 				centre_cella 	# index del mapa de la cel·la corresponent al centre

geometry_msgs/Point centre_lliure_punt	# posició lliure més propera al centre de la frontera
uint32 				centre_lliure_cella	# index del mapa de la cel·la corresponent a centre_lliure

geometry_msgs/Point[] 	celles_punts 	# vector amb la posició de totes les cel·les de la frontera 
uint32[] 				celles_celles 	# vector amb els indexs del mapa de les cel·les de la frontera