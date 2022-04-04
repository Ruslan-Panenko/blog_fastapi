import datetime

from fastapi import APIRouter, Depends
from newsapi import NewsApiClient
from sqlalchemy.orm import Session
from database import get_db
from posts import models
from posts.schemas import Post
from users import auth

now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d")

router = APIRouter(prefix='/parse')
newsapi = NewsApiClient(api_key='fa2093168b0740e591d92b3264690ab9')
all_articles = newsapi.get_everything(q='ukraine',
                                      from_param=current_date,
                                      to='2021-10-06',
                                      sort_by='relevancy',
                                      )


@router.post('/',)
async def create_post(db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    all_posts = db.query(models.Post.title).all()

    posts = []
    for i in all_posts:
        posts.append(i.title)
    for post in all_articles['articles']:
        new_post = models.Post(title=post['title'], content=post['content'], published=True,
                               owner_id=current_user)
        if new_post.title not in posts:

            db.add(new_post)
            db.commit()
            db.refresh(new_post)

    return {'data': all_posts}