from typing import Optional
from comments.models import Comment
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from . import models
from .schemas import Post
from users import auth

router = APIRouter(prefix='/posts', tags=['Posts'])


def raise_error(post):
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content was not found')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user),
                    limit: int = None,
                    skip: int = 0,
                    search: Optional[str] = ''):
    posts = db.query(models.Post) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(skip) \
        .all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    raise_error(post)
    comments = db.query(Comment).filter(Comment.post_id == id).all()

    return Post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = delete_post_query.first()
    raise_error(delete_post)
    if delete_post.owner_id != int(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized')

    delete_post_query.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}')
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db),
                      current_user: int = Depends(auth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    raise_error(post)
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post
