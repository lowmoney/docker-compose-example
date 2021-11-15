from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel
from deta import Deta

deta = Deta('b063huxq_puJ1My3CiVDT3UfH5BWG5wKWuHt7Q2es')
db = deta.Base('products')

router = APIRouter(
    prefix="/api",
    tags=['products']
)

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
    name: Optional[str] = None
    price: Optional[float] = None

class DeleteProduct(BaseModel):
    key: Optional[str] = 'product_key'
    deleted: Optional[bool] = True

@router.get("/")
async def read_root():
    return {
        'Welcome': 'Hello World!',
        'Doc': 'api/docs',
        'Endpoints': [
            {            
                "api/get_products": {
                    'method':'GET',
                    'description':'send a GET request to this endpoint to get all the Products in the DB'
                    },
                "api/add_product": {
                    'method':'POST',
                    'params': {'name':True, 'price':True},
                    'description':'send a POST request to this endpoint with params to add a product'
                    },
                "api/edit_product": {
                    'method':'PUT',
                    'params': {'key':True,'name':False,'price':False},
                    'description': 'send a PUT request to this endpoint with params to update product of param key'
                    },
                "api/delete_product": {
                    'method': 'DELETE',
                    'params': {'key':True},
                    'description': 'send a DELETE request to this endpoint with the requiered param key'
                    }
            }
            ]
        }


@router.get("/get_products")
async def get_product():
    products = db.fetch()
    return Products(**{"products":products.items})    

@router.post("/add_product", response_model=Product)
async def add_product(product:AddProduct):
    added = {"key":'already_exists', 'name':'product not added', 'price':0}
    try:
        added = db.insert(dict(product))
    except:
        pass

    return Product(**added)

@router.put("/edit_product", response_model=Product)
async def edit_product(product:EditProduct):
    added = {"key":"missing key", 'name':'product not found', 'price':0}
    if product.key:
        if product.name:
            db.update({'name': product.name}, product.key)
        elif product.price:
            db.update({'price': product.price}, product.key)
        else:
            added = {"key":product.key, 'name':'no product name given (need name and/or price)', 'price':'no pirce given (need name and/or price)'}
        added = db.get(product.key)

    return Product(**added)

@router.delete("/delete_product", response_model=DeleteProduct)
async def delete_product(product:DeleteProduct):
    if product.key:
        product = db.delete(product.key)

    return DeleteProduct()