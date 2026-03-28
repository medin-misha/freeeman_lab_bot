from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Result, String, or_, and_, Boolean, Integer, DateTime, Date, Float
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from pydantic import BaseModel
from datetime import datetime

from typing import TypeVar, Type, Union
import logging

from .error_handlers import DBErrorHandler

# универсальные дженерики
ModelT = TypeVar("ModelT", bound=DeclarativeBase)
SchemaT = TypeVar("SchemaT", bound=BaseModel)
logger = logging.getLogger(__name__)


class CRUD:
    @staticmethod
    async def create(
        data: SchemaT, model: Type[ModelT], session: AsyncSession
    ) -> ModelT:
        """
        💡 Универсальное создание ORM-сущности.

        Создаёт новую запись в базе данных из Pydantic-схемы.
        Все ошибки SQLAlchemy автоматически обрабатываются DBErrorHandler.

        Args:
            data: Входная Pydantic-модель с данными.
            model: ORM-модель (дочерний класс Base).
            session: Асинхронная сессия SQLAlchemy.

        Returns:
            Созданный ORM-объект после refresh().

        Raises:
            HTTPException: при любой ошибке БД или некорректных данных.
        """
        instance = model(**data.model_dump())
        try:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        except HTTPException:
            raise
        except Exception as err:
            await session.rollback()
            DBErrorHandler.handle(err=err, model=model)
        else:
            return instance

    @staticmethod
    async def get(
        model: Type[ModelT],
        session: AsyncSession,
        id: int | None = None,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        field: str | None = None,
    ) -> Union[ModelT, list[ModelT]]:
        """
        💡 Универсальный метод чтения данных из базы.

        Если передан `id`, возвращает одну запись по первичному ключу.
        Если `id` не указан — возвращает список всех записей модели.

        Args:
            model: ORM-модель (дочерний класс Base)
            session: асинхронная сессия SQLAlchemy
            id: идентификатор записи (опционально)
            page: страница (опционально)
            limit: лимит (опционально)
            search: поисковый запрос (опционально)
            fields: поля для поиска (опционально)

        Returns:
            Один объект модели или список всех объектов.

        Raises:
            HTTPException(404): если запись по id не найдена.
            HTTPException(400/503/500): если произошла SQL-ошибка (через DBErrorHandler).
        """
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10
        try:
            stmt = select(model)
            mapper: Mapper = inspect(model)
            model_columns = {column.name: column for column in mapper.columns}
            if id is not None:
                stmt = stmt.where(model.id == id)
            elif search:
                if field is not None:
                    if field not in model_columns.keys():
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Field '{field}' not found in {model.__name__}")
                    model_field = getattr(model, field)
                    stmt = stmt.where(model_field == CRUD.parse_value(mapper.columns[field], search))
                else:
                    words = search.strip().split()
                    columns = []
                    word_conditions = []
                    for column in model_columns.values():
                        if isinstance(column.type, String):
                            columns.append(column)
                    for word in words:
                        word_pattern = f"%{word}%"
                        field_conditions = [col.ilike(word_pattern) for col in columns]
                        word_conditions.append(or_(*field_conditions))
                    stmt = stmt.where(and_(*word_conditions))
            stmt = stmt.limit(limit).offset((page - 1) * limit)
            result: Result = await session.execute(stmt)
            data = result.scalars().all()
            if id is not None:
                if not data:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{model.__name__} with id={id} not found.",
                    )
                return data[0]
            return data
        except HTTPException:
            raise
        except Exception as err:
            # Любая ошибка SQLAlchemy или инфраструктуры
            DBErrorHandler.handle(err=err, model=model)

    @staticmethod
    async def patch(
        new_data: SchemaT,
        model: Type[ModelT],
        session: AsyncSession,
        id: int,
    ) -> ModelT:
        """
        💡 Универсальное обновление записи (частичное).

        Обновляет только те поля, которые переданы в Pydantic-модели `new_data`.
        Если запись с указанным id не найдена, выбрасывает 404.
        Все ошибки SQLAlchemy обрабатываются через DBErrorHandler.

        Args:
            new_data: Pydantic-модель с обновлёнными полями
            model: ORM-модель
            session: асинхронная сессия SQLAlchemy
            id: идентификатор записи

        Returns:
            Обновлённый ORM-объект

        Raises:
            HTTPException(404): если запись не найдена
            HTTPException(400/503/500): при ошибках БД
        """
        try:
            stmt = select(model).where(model.id == id)
            result: Result = await session.execute(stmt)
            instance = result.scalars().first()

            if not instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{model.__name__} with id={id} not found.",
                )

            # exclude_unset → обновляем только реально переданные поля
            update_data = new_data.model_dump(exclude_unset=True)

            # Защита: не даём обновить первичный ключ
            update_data.pop("id", None)

            for field, value in update_data.items():
                setattr(instance, field, value)

            await session.commit()
            await session.refresh(instance)

            return instance
        except HTTPException:
            raise
        except Exception as err:
            await session.rollback()
            DBErrorHandler.handle(err=err, model=model, action="updating")

    @staticmethod
    async def delete(
        model: Type[ModelT],
        session: AsyncSession,
        id: int,
    ) -> str:
        """
        💡 Удаляет запись по ID.

        Args:
            model: ORM-модель (дочерний класс Base)
            session: асинхронная сессия SQLAlchemy
            id: идентификатор записи для удаления

        Returns:
            Строка `"ok"` при успешном удалении.

        Raises:
            HTTPException(404): если запись не найдена
            HTTPException(400/503/500): при ошибках БД (через DBErrorHandler)
        """
        try:
            stmt = select(model).where(model.id == id)
            result: Result = await session.execute(stmt)
            instance: ModelT | None = result.scalars().first()

            if not instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{model.__name__} with id={id} not found.",
                )

            await session.delete(instance)
            await session.commit()
            return "ok"
        except HTTPException:
            raise
        except Exception as err:
            await session.rollback()
            DBErrorHandler.handle(err=err, model=model, action="deleting")
    
    @staticmethod
    async def bulk_create(
        data: list[SchemaT], model: Type[ModelT], session: AsyncSession
    ) -> list[ModelT]:
        instances = [model(**item.model_dump()) for item in data]
        try:
            session.add_all(instances)
            await session.commit()
            for instance in instances:
                await session.refresh(instance)
        except HTTPException:
            raise
        except Exception as err:
            await session.rollback()
            DBErrorHandler.handle(err=err, model=model)
        else:
            return instances

    @staticmethod
    def parse_value(column, raw_value: str):
        column_type = column.type
        boolean_map = {
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False,
                    "yes": True,
                    "no": False,
                }
        try:
            # STRING
            if isinstance(column_type, String):
                return raw_value

            # INTEGER
            elif isinstance(column_type, Integer):
                return int(raw_value)

            # FLOAT
            elif isinstance(column_type, Float):
                return float(raw_value)

            # BOOLEAN
            elif isinstance(column_type, Boolean):

                value = raw_value.lower()
                if value not in boolean_map:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid value '{raw_value}' for field '{column.name}'"
                    )

                return boolean_map[value]

            # DATE
            elif isinstance(column_type, Date):
                return datetime.strptime(raw_value, "%Y-%m-%d").date()

            # DATETIME
            elif isinstance(column_type, DateTime):
                return datetime.fromisoformat(raw_value)

            # fallback
            return raw_value

        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value '{raw_value}' for field '{column.name}'"
            )