from math import prod
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from deta import Deta
from nanoid import generate

deta = Deta('b063huxq_puJ1My3CiVDT3UfH5BWG5wKWuHt7Q2es')
db = deta.Base('products')

app = FastAPI()

class Product(BaseModel):
    key: str
    name: str
    price: float

class Products(BaseModel):
    products: List[Product]

class AddProduct(BaseModel):
    name: str
    price: float

class EditProduct(BaseModel):
    key: str
    name: Optional[str]
    price: Optional[float]

class DeleteProduct(BaseModel):
    key: Optional[str] = 'product_key'
    deleted: Optional[bool] = True

@app.get("/")
def read_root():
    return {"helo": "world"}

@app.get("/get_products", response_model=Products)
def get_product():
    products = db.fetch()
    return Products(**{"products":products.items})

@app.post("/add_product", response_model=Product)
def add_product(product:AddProduct):
    added = {"key":'already_exists', 'name':'product not added', 'price':0}
    try:
        added = db.insert(dict(product))
    except:
        pass

    return Product(**added)

@app.put("/edit_product", response_model=Product)
def edit_product(product:EditProduct):
    added = {"key":None, 'name':'product not found', 'price':0}
    if product.key:
        try:
            if product.name != 'string':
                db.put({'name': product.name}, product.key)
            if product.price != -1:
                db.put({'price': product.price}, product.key)
            added = db.get(product.key)
        except:
            pass
    
    print(added)
    return Product(**added)

@app.delete("delete_product", response_model=DeleteProduct)
def delete_product(product:DeleteProduct):
    if product.key:
        product = db.delete()

    return DeleteProduct()