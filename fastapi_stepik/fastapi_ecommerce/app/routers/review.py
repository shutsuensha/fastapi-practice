from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update
from app.schemas import CreateCategory, CreateReview, CreateRating
from app.routers.auth import get_current_user
from slugify import slugify 

router = APIRouter(prefix='/review', tags=['review'])


@router.get('/all_reviews')
async def get_all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    return reviews.all()


@router.get('/products_reviews')
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)], slug: str):
    product = await db.scalar(
        select(Product).where(Product.slug == slug, Product.is_active == True, Product.stock > 0))
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    reviews = await db.scalars(select(Review).where(Review.is_active == True, Review.product_id == product.id))
    return reviews.all()


@router.post('/add_review')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)], create_review: CreateReview, product_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_customer'):
        product = await db.scalar(
                        select(Product).where(Product.id == product_id, Product.is_active == True, Product.stock > 0))
        if not product:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There are no product'
            )
        
        
        rating_result = await db.execute(
                insert(Rating)
                .values(grade=create_review.rating.grade,
                        user_id=get_user.get('id'),
                        product_id=product.id)
                .returning(Rating.id)
        )


        rating_id = rating_result.scalar()

        
        all_ratings_by_product = await db.scalars(select(Rating).where(Rating.is_active == True, Rating.product_id == product.id))
        all_ratings_by_product = all_ratings_by_product.all()
        new_product_rating = sum([el.grade for el in all_ratings_by_product]) / len(all_ratings_by_product)

        await db.execute(update(Product).where(Product.id == product.id).values(rating=new_product_rating))

        review = await db.execute(insert(Review).values(comment=create_review.comment,
                                           user_id=get_user.get('id'),
                                           product_id=product.id,
                                           rating_id=rating_id))
        
        await db.commit()
        

        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You must be customer user for this'
        )


@router.delete('/delete_reviews')
async def delete_review(db: Annotated[AsyncSession, Depends(get_db)], product_id: int, review_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        product = await db.scalar(
                        select(Product).where(Product.id == product_id, Product.is_active == True, Product.stock > 0))
        if not product:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There are no product'
            )
        
        review = await db.scalar(
                        select(Review).where(Review.id == review_id, Review.is_active == True))
        if not review:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There are no review'
            )
        
        await db.execute(update(Rating).where(Rating.id == review.rating_id).values(is_active=False))
        await db.execute(update(Review).where(Review.id == review.id).values(is_active=False))

        all_ratings_by_product = await db.scalars(select(Rating).where(Rating.is_active == True, Rating.product_id == product.id))
        all_ratings_by_product = all_ratings_by_product.all()
        new_product_rating = sum([el.grade for el in all_ratings_by_product]) / len(all_ratings_by_product)

        await db.execute(update(Product).where(Product.id == product.id).values(rating=new_product_rating))

        await db.commit()
        

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Review delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You must be admin user for this'
        )