import pickle

route_info = dict()

route_info['dag 1'] = ['Dag 1 - 15 km','Van Baraque Fraiture/Plateau des Tailles naar Houffalize via de GR15. We overnachten op Camping Chasse et Pêche.']
route_info['dag 2'] = ['Dag 2 - 18 km','Camping Chasse et Pêche (Houffalize) - Nadrin via Escapardenne Eislektrail. We overnachten op camping Belle-Meuse.']
route_info['dag 3'] = ['Dag 3 - 20 km','Nadrin – La Roche: via Eislektrail/GR57 met spectaculaire wandelingen over de rotskam Le Herou en langs de Keltische versterking Le Cheslé. We overnachten op Camping du Vieux Moulin (Petite Strument).']
#route_info['dag 4 kort'] = ['Dag 4 kort - 15/24 km','La Roche – Nassonge via Bande']
#route_info['dag 4 lang'] = ['Dag 4 lang - 27 km','La Roche – Nassonge via Bande. We overnachten op Camping Fontaine Monseu.']
route_info['dag 4'] = ['Dag 4 - 24 of 27 km','Let op! De blauwe route is de lange route. We lopen van La Roche – Nassonge via Bande. De overnachting voor de 6-daagse tour vindt plaats op Camping Fontaine Monseu.']
route_info['dag 5'] = ['Dag 5 - 21 of 28 km','Nassonge-Saint Hubert. We overnachten op Camping Europacamp.']
route_info['dag 6'] = ['Dag 6 - 11 km','Saint Hubert- Camping Tonny via o.a. GR14.']

pickle_out = open("route_info.pickle","wb")
pickle.dump(route_info,pickle_out)
pickle_out.close()

#print(route_info['dag 4 lang'][1])
