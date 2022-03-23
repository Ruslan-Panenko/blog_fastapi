from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from posts import models
from posts.schemas import Post
from users import auth

router = APIRouter(prefix='/posts', tags=['Posts'])


def raise_error(post):
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content was not found')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    raise_error(post)

    return {'data': post}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    raise_error(delete_post)
    delete_post.delete(synchronize_session=False)
    db.commit()
    return {'data': "post was successfully deleted"}


@router.put('/{id}')
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db),
                      user_id: int = Depends(auth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    raise_error(post)

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {'data': 'successful'}
