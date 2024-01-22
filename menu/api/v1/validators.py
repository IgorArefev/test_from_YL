from fastapi import HTTPException, status
from sqlalchemy import select


class Validators:
    def __init__(self, model):
        self.model = model

    async def uniq_name_check(self, name, session):
        duplicate = await session.execute(
            select(self.model).where(self.model.title == name)
        )
        duplicate = duplicate.scalars().first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="already exist"
            )

    async def id_object_exist(self, _id, session):
        item = await session.execute(
            select(self.model).where(self.model.id == _id)
        )
        return item.scalars().first()
