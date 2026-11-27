import asyncpg

_pool: asyncpg.Pool | None = None


async def create_db_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        user="u0_a54",
        password="abcd+123456789",
        database="mfhm",
        host="127.0.0.1",
        port=5432,
        min_size=1,
        max_size=5,
    )


async def init_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await create_db_pool()
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool has not been initialized. Call await init_pool() first.")
    return _pool

async def session_token_is_valid(session_token: str | None) -> bool:
    if session_token is None:
        return False
    pool = get_pool()
    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "SELECT 1 FROM sessions WHERE token = $1",
            session_token,
        )
    return row is not None