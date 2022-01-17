from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('zooanimals', user='postgres', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Zooanimal(BaseModel):
  name = CharField()
  animal_type = CharField()
  lifespan = IntegerField()
  habitat = CharField()
  diet = CharField()

db.connect()
db.drop_tables([Zooanimal])
db.create_tables([Zooanimal])

Angolan_Python = Zooanimal(name='Angolan Python', animal_type='Reptile', lifespan=30, habitat='Arid rocky areas and bushland', diet='Rodents and birds')
Yellow_Banded_Poison_Dart_Frog = Zooanimal(name='Yellow Banded Poison Dart Frog', animal_type='Amphibian', lifespan=7, habitat='Tropical rainforest', diet='Insects, spiders, and other small invertebrates')
Titicaca_Water_Frog = Zooanimal(name='Titicaca Water Frog', animal_type='Amphibian', lifespan=20, habitat='Freshwater lakes and welands', diet='Crustaceans, snails, and other small animals')
Masked_Lapwing = Zooanimal(name='Masked Lapwing', animal_type='Bird', lifespan=16, habitat='Wetlands and grasslands', diet='Worms and insects')
Timber_Rattlesnake = Zooanimal(name='Timber Rattlesnake', animal_type='Reptile', lifespan=20, habitat='Rocky hillsides, fields, woodlands and swamp', diet='Small mammals, birds, reptiles and amphibians')

Angolan_Python.save()
Yellow_Banded_Poison_Dart_Frog.save()
Titicaca_Water_Frog.save()
Masked_Lapwing.save()
Timber_Rattlesnake.save()

app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def hello():
#   return 'Hello'

@app.route('/zooanimals',  methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/zooanimals/<id>',  methods=['GET', 'POST', 'PUT', 'DELETE'])
def zooanimals(id=None):
  if request.method == 'GET':
    if id:
      animal = Zooanimal.get(Zooanimal.id == id)
      animal = model_to_dict(animal)
      return jsonify(animal)
    else:
      animals = []
      for animal in Zooanimal.select():
        animals.append(model_to_dict(animal))
      return jsonify(animals)
  
  if request.method == 'POST':
    zooanimal = request.get_json()
    zooanimal = dict_to_model(Zooanimal, zooanimal)
    zooanimal.save()
    zooanimal = model_to_dict(zooanimal)
    zooanimal = jsonify(zooanimal)
    return zooanimal
  
  if request.method == 'DELETE':
    zooanimal = Zooanimal.get(Zooanimal.id == id)
    zooanimal.delete_instance()
    return jsonify({"deleted": True})

  if request.method == 'PUT':
    update_animal = request.get_json()
    zooanimal = Zooanimal.get(Zooanimal.id == id)
    zooanimal.name = update_animal['name']
    zooanimal.animal_type = update_animal['animal_type']
    zooanimal.lifespan = update_animal['lifespan']
    zooanimal.habitat = update_animal['habitat']
    zooanimal.diet = update_animal['diet']
    zooanimal.save()
    zooanimal = model_to_dict(zooanimal)
    zooanimal = jsonify(zooanimal)
    return zooanimal

app.run(port=9000, debug=True)