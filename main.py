#FastAPI Practice
#
#pip install fastapi
#Fast API includes multiple interactive documentation pages: http://127.0.0.1:8000/docs
# and http://127.0.0.1:8000/redoc
#pros and cons comparing Fast API to Flask
#Flask has higher support, Fast API is newer though 
#Similar comparisons to Django, though Django is a higher weight
#pip install uvicorn- the server used to test the application
#to test the app using uvicorn, in the terminal, type: uvicorn main:app --reload
#main because that is the file name, app because that's what the app as been defined as
#--reload flag makes the server refresh every time you update the file

#HTTPException allows us to raise exceptions
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

#define the app
app = FastAPI()

#pydantic used here:
class Item(BaseModel):
    text: str = None
    is_done: bool = False

#the empty list for the items to populate
items = []

#defining the first path
#this is the root directory
#again, to view on the uvicorn server, in the terminal:
#uvicorn main:app --reload (--reload is optional)
@app.get("/")
def root():
    return{"hello": "world"}

#post request to add items to the list
#returns the full items list with all items
#to add items to the list, in the terminal: 
#curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=[ITEM NAME]

#once we add the item Class, it changes the item to be the JSON payload of the request
#and it needs to be updated differently, you need to send the item data as the payload
# curl -X POST -H "Content-Type: application/json" -d '{"text":"[ITEM NAME]"}' 'http://127.0.0.1:8000/items'
#this returns an object that conforms to our Item model defined above
#as such, it needs to be {"text":"..."} because text is how it was defined in the Item class
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items


#using a get endpoint to get all items on the list
#to access, use the get request in the terminal:
#curl -X GET 'http://127.0.0.1:8000/items?limit=3'
@app.get("/items", response_model=list[Item])
#limit parameter is used to limit how many items are returned
def list_items(limit: int = 10):
    return items[0:limit]

#using a get endpoint to get a specific item
#to access, use the get request in the terminal:
#curl -X GET http://127.0.0.1:8000/item/[INDEX OF THE ITEM YOU WANT]
#adding the response model makes it easier to work with front end framework because it
#creates a defined response structure that is reliable
@app.get("/items/{item_id}", response_model=Item)
def get_items(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        #raises a 404 Error if you try to access an item that is out of range of the list
        #detail parameter can be used to give more information about what wasn't found
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


