from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Union, Optional, List
from src.core import logger
from bson import ObjectId
from src.exceptions import UnknownTableException, QueryException
import re
from traceback import format_exc

OP_MAP = {
    '=': lambda k, v: {k: v},
    '<': lambda k, v: {k: {'$lt': v}},
    '>': lambda k, v: {k: {'$gt': v}},
    '<=': lambda k, v: {k: {'$lte': v}},
    '>=': lambda k, v: {k: {'$gte': v}},
    '!=': lambda k, v: {k: {'$ne': v}},
}


class BaseMongoRepository:
    """Base repository for MongoDB operations following Clean Code principles."""

    COLLECTION_NAME: str

    def __init__(self, client: AsyncIOMotorClient, database_name: str):
        self.client = client
        self.db_name = database_name

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Get MongoDB collection by name."""
        if not self.COLLECTION_NAME:
            logger.error(f'Missing COLLECTION_NAME: {format_exc()}')
            raise UnknownTableException()
        return self.client[self.db_name][self.COLLECTION_NAME]

    # CRUD OPERATIONS
    async def add(self,
                  document: dict,
                  fetch: bool = False) -> Union[dict, None]:
        """
        Insert a single document into the collection.

        Args:
            document: Dictionary to insert
            fetch: If True, returns the inserted document

        Returns:
            Inserted document (if fetch=True) or ObjectId
        """
        try:
            result = await self.collection.insert_one(document)
            logger.info(
                f"Added document to {self.collection} with id: {result.inserted_id}")

            if fetch:
                return await self.collection.find_one({"_id": result.inserted_id})

        except Exception:
            logger.error(f'Error adding to {self.collection}: {format_exc()}')
            raise QueryException()

    async def add_many(self,
                       documents: List[dict]) -> List[ObjectId]:
        """
        Insert multiple documents into the collection.

        Args:
            documents: List of dictionaries to insert

        Returns:
            List of inserted ObjectIds
        """
        try:
            result = await self.collection.insert_many(documents)
            logger.info(
                f"Added {len(result.inserted_ids)} documents to {self.collection}")
            return result.inserted_ids

        except Exception:
            logger.error(
                f'Error adding multiple data to {self.collection}: {format_exc()}')
            raise QueryException()

    async def update(self,
                     filters: dict,
                     values: dict,
                     upsert: bool = False,
                     fetch: bool = True) -> Union[dict, None]:
        """
        Update documents in the collection.

        Args:
            filters: Query filters to match documents
            values: Values to update
            upsert: If True, insert if document doesn't exist
            fetch: If True, returns the updated document

        Returns:
            Updated document (if fetch=True)
        """
        try:
            update_doc = {"$set": values}

            result = await self.collection.update_one(filters, update_doc, upsert=upsert)
            logger.info(
                f"Updated {result.modified_count} document(s) in {self.collection}")

            if fetch:
                return await self.collection.find_one(filters)

        except Exception:
            logger.error(f'Error updating {self.collection}: {format_exc()}')
            raise QueryException

    async def select_data(self,
                          filters: Optional[dict] = None,
                          projection: Optional[dict] = None,
                          sort: Optional[List[tuple]] = None,
                          limit: Optional[int] = None,
                          return_all: bool = False) -> Union[dict, List[dict], None]:
        """
        Select documents from the collection.

        Args:
            filters: Query filters
            projection: Fields to select
            sort: Sort criteria [(field, direction), ...]
            limit: Maximum number of documents to return
            return_all: Whether to return all results or just the first

        Returns:
            Document(s) matching the criteria
        """
        try:
            cursor = self.collection.find(filters or {}, projection)

            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)

            logger.debug(
                f'Select query on {self.collection} with filters: {filters}')

            if return_all:
                return await cursor.to_list(length=None)
            try:
                return await cursor.next()
            except StopAsyncIteration:
                return []
        except Exception:
            logger.error(
                f'Error selecting data from {self.collection}: {format_exc()}')
            raise QueryException()

    async def upsert(self,
                     filters: dict,
                     values: dict,
                     fetch: bool = False) -> Union[dict, None]:
        """
        Performs an UPSERT (insert or update) operation.

        Args:
            filters: Query filters to match existing document
            values: Values to insert/update
            fetch: If True, returns the upserted document

        Returns:
            Upserted document (if fetch=True)
        """
        if not filters:
            raise ValueError("Filters cannot be empty for upsert operation.")

        return await self.update(
            filters=filters,
            values=values,
            upsert=True,
            fetch=fetch
        )

    @staticmethod
    def parse_filter_expr(expr: str, values: dict) -> dict:
        if not any(_ in expr for _ in ['AND', 'OR']):
            logic = None
        else:
            logic = 'AND' if 'AND' in expr else 'OR'
        parts = re.split(r'\s+(AND|OR)\s+', expr)
        filters = []
        for part in parts:
            if part in ('AND', 'OR'):
                continue
            m = re.match(r'([a-zA-Z_]\w*)\s*(=|<|>|<=|>=|!=)\s*(\w+)',
                         part.strip())
            if not m:
                raise ValueError(f"Invalid expression: {part}")
            k, op, v = m.groups()
            filters.append(OP_MAP[op](k, values[v]))
        if logic == 'AND':
            return {'$and': filters}
        elif logic == 'OR':
            return {'$or': filters}
        else:
            return filters[0]
