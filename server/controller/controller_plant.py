from models import Plant, db



def  update_plant(plant_id:int,name:str, image:str, price:float, is_in_stock:bool):
    plant = db.session.get(Plant, plant_id)
    if not plant:
        return {"error": "Plant not found"}, 404

    plant.name = name
    plant.image = image
    plant.price = price
    plant.is_in_stock = is_in_stock

    db.session.commit()
    return plant.to_dict(), 200 


def patch_plant(plant_id:int, data:dict):
    plant = db.session.get(Plant, plant_id)
    if not plant:
        return {"error": "Plant not found"}, 404

    if 'name' in data:
        plant.name = data['name']
    if 'image' in data:
        plant.image = data['image']
    if 'price' in data:
        plant.price = data['price']
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']

    db.session.commit()
    return plant.to_dict(), 200


def delete_plant(plant_id:int):
    plant = db.session.get(Plant, plant_id)
    if not plant:
        return {"error": "Plant not found"}, 404

    db.session.delete(plant)
    db.session.commit()
    return "", 204