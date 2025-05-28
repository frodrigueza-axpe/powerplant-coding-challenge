from clases.exceptions import ExceptionErroCheckJSON

class Utils:
    
    def checkJsonValid(data):
        
        json_respuesta = {
            "error": False 
            , "message": ""
        }
        
        required_keys = {"load", "fuels", "powerplants"}
        
        try:
            if not required_keys.issubset(data.keys()):
                
                json_respuesta["error"] = True
                json_respuesta["message"] = "Missing required fields"
                return json_respuesta

            json_respuesta["error"] = False
            json_respuesta["data"] = data
        except:
            raise ExceptionErroCheckJSON("Error check Json")
        
        return json_respuesta
    
    
    
    