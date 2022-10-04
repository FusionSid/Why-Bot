""" (module) asyncpg_context
Context manager for asyncpg
"""

from contextlib import asynccontextmanager

import asyncpg


@asynccontextmanager
async def asyncpg_connect(database_url: str) -> asyncpg.connection.Connection:
    """
    Custom context manager to use asyncpg
    Very useful to ensure that once I open a connection it will ALWAYS be closed even upon error

    Parameters:
        database_url: str: The connection string

    Yeilds:
        asyncpg.connection.Connection: The connection to the database
    """
    # Connect to the database
    connection = await asyncpg.connect(database_url)

    # Return connection for with statement
    yield connection

    # close connection once context manager is closed
    await connection.close()
