from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My AI API Server", version="1.0.0")
 
 # Get kommandoer som giver simple endpoints fx som beskeder. 
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/secret")
def get_secret():
    return {"Message": "You found my secret!"}


####################################################################################

# Her kan vi lave endpoints som tager parametre via URL
@app.get("/add/{a}/{b}")
def add_numbers(a: int, b: int):
    result = a + b
    return {"a": a, "b": b, "result": result}
# Når vi tilgår URL http://127.0.0.1:8000/add/5/7 så får vi resultatet 12 tilbage på en pæn måde. 



# Her kan vi lave endpoints som tager parametre efter et spørgsmålstegn
@app.get("/multiply/")
def multiply_numbers(a: int, b: int):
    result = a * b
    return {"a": a, "b": b, "result": result}

#Når vi kører URL igennem som http://127.0.0.1:8000/multiply/?a=3&b=4 så får vi resultatet 12 tilbage på en pæn måde. 


#Forskellen på de to er at path parameters er værdier der er en del af stien 
#Hvor
# Query parameters er værdier som indslttes efter ?
####################################################################################


# Laver en simpel API til at udføre grundlæggende matematiske operationer
class Item(BaseModel):
    number1: float
    number2: float

# Post som giver data ind/ud
@app.post("/subtract/")
def subtract(item: Item):
    return {"resultat": item.number1 - item.number2}

@app.post("/multiply/")
def multiply(item: Item):
    return {"resultat": item.number1 * item.number2}

@app.post("/divide/")
def divide(item: Item):
    if item.number2 == 0:
        return {"error": "Kan ikke dividere med nul!"}
    return {"resultat": item.number1 / item.number2}







if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Server:app", host="127.0.0.1", port=8000, reload=True)
