from flask import jsonify, request
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app()

# Token para poder hacer uso de ciertas funciones.
key = "MissingNo151"


# Ruta y función para poder obtener toda la información de la API.
@app.route('/all_teams/', methods=['GET'])
def show_teams():
    all_teams = dumps(list(db.db.MakeTeams.find()))
    return all_teams

#Ruta y función para poder obtener información de un usuario en específico en base en su nombre de la API.
@app.route(f'/MakeTeams/<string:n_key>/', methods=['GET'])
def show_a_team(n_key):
    team = dumps(db.db.MakeTeams.find_one({'user_name':n_key}))
    return team

# Ruta y función para agregar un equipo a la API con un nuevo JSON.
@app.route(f'/{key}/new_team/', methods=['POST'])
def add_new_team():
    
    db.db.MakeTeams.insert_one ( {
				"poke_id0" : request.json["poke_id0"],
				"poke_id1" : request.json["poke_id1"],
				"poke_id2" : request.json["poke_id2"],
				"poke_id3" : request.json["poke_id3"],
				"poke_id4" : request.json["poke_id4"],
				"poke_id5" : request.json["poke_id5"],
				"user_name" : request.json["user_name"]
			})
    return jsonify({
        "message":"Equipo añadido",
        "status": 200,
    })

# Ruta y función para actualizar la información de un usuario en base a su nombre de la API con un nuevo JSON.
@app.route(f'/{key}/MakeTeams/update/<string:n_key>',methods=['PUT'])
def update_team(n_key):

    if db.db.MakeTeams.find_one({'user_name':n_key}):
        db.db.MakeTeams.update_one({'user_name':n_key},
        {'$set':{
                "poke_id0" : request.json["poke_id0"],
				"poke_id1" : request.json["poke_id1"],
				"poke_id2" : request.json["poke_id2"],
				"poke_id3" : request.json["poke_id3"],
				"poke_id4" : request.json["poke_id4"],
				"poke_id5" : request.json["poke_id5"],
				"user_name" : request.json["user_name"]
        }})
    else:
        return jsonify({"status":400, f"equipo {n_key} no encontrado"})

    return jsonify({"status":200,f"el equipo{n_key} fue actualizado"})

# Ruta y función para eliminar un usuario en base a su nombre de la API.

@app.route(f'/{key}/MakeTeams/del/<string:n_key>',methods=['DELETE'])
def delete_team(n_key):
    if db.db.MakeTeams.find_one({'user_name':n_key}):
        db.db.MakeTeams.delete_one({'user_name':n_key})
    else:
        return jsonify({"status":400,  f"equipo {n_key} no encontrado"})
    return jsonify({"status":200,f"el equipo {n_key} fue eliminado"})

# # Verificación para saber si el archivo es el main, si es el caso se ejecutará app.run.
if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)
