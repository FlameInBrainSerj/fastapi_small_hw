from enum import Enum
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing_extensions import Literal
from typing import Any, List

from datetime import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root() -> str:
    return 'Hello, (wo)man and any other non-binary creature!'


@app.post('/post', response_model=Timestamp, summary='Get Post')
def get_post() -> Timestamp:
    post = Timestamp(
        id=post_db[-1].id + 1,
        timestamp=int(datetime.now().timestamp())
    )
    post_db.append(post)
    return post


@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dogs(kind: Literal['terrier', 'bulldog', 'dalmatian'] = None) -> List[Dog]:
    if kind is None:
        return list(dogs_db.values())
    return [
        dogs_db[key]
        for key in dogs_db.keys()
        if dogs_db[key].kind == kind
    ]


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog) -> Dog:
    if dog.pk in dogs_db:
        raise HTTPException(
            status_code=409,
            detail='The specified PK already exists.'
        )
    dogs_db[list(dogs_db.keys())[-1] + 1] = dog
    return dog


@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dogs_by_pk(pk: int) -> Dog:
    if pk in dogs_db:
        return value
    raise HTTPException(
                status_code=409,
                detail='Dogs with the specified PK foes does not exist.'
    )


@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, dog: Dog) -> Dog:
    for key, value in dogs_db.items():
        # We can only update the name and the kind of dog, but not his pk
        if value.pk == pk and dog.pk == pk:
            dogs_db[key] = dog
            return dog
    raise HTTPException(
        status_code=409,
        detail='Your path PK and request body PK are not the same'
    )
