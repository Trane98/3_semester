from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My AI API Server", version="1.0.0")
 
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/secret")
def get_secret():
    return {"Message": "You found my secret!"}


# Laver en simpel API til at udføre grundlæggende matematiske operationer
class Item(BaseModel):
    number1: float
    number2: float


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
