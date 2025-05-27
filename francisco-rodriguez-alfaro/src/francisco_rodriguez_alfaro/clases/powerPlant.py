


class FieldName():
    
    load = "load"
    gas = "gas(euro/MWh)"
    kerosine = "kerosine(euro/MWh)"
    co2 = "co2(euro/ton)"
    wind = "wind(%)"
    
    name = "name"
    type = "type"
    efficiency = "efficiency"
    pmin = "pmin"
    pmax = "pmax"
    


class Fuel():
    
    def __init__(self, data_object_fuels):
        self.gas = data_object_fuels.get(FieldName.gas)
        self.kerosine = data_object_fuels.get(FieldName.kerosine)
        self.co2 = data_object_fuels.get(FieldName.co2)
        self.wind = data_object_fuels.get(FieldName.wind)

class PowerPlant():
    
    def __init__(self, data_object_powerplant):
        
        self.name = data_object_powerplant.get(FieldName.name)
        self.type = data_object_powerplant.get(FieldName.type)
        self.efficiency = data_object_powerplant.get(FieldName.efficiency)
        self.pmin = data_object_powerplant.get(FieldName.pmin)
        self.pmax = data_object_powerplant.get(FieldName.pmax)
        
        pass 
        

class ResumePowerPlant:

    load = None 
    fuels = None 
    powerplants = None

    def __init__(self, data):
        
        data_object = data.get("data")
        
        self.load = data_object.get(FieldName.load)
        self.fuels = ResumePowerPlant.get_fuels(data_object.get("fuels"))
        self.powerplants = ResumePowerPlant.get_powerplants(data_object.get("powerplants"))
        
    def get_fuels(data_object_fuels):
        
        fuel = Fuel(data_object_fuels)
        return fuel
        
    
    def get_powerplants(data_object_powerplants):
        
        powerplants = []
        for plant in data_object_powerplants:
            
            obj_plan = PowerPlant(plant)
            powerplants.append(obj_plan)
            
        return powerplants
        
        
        
        
        
        
        


