import tomllib
from psycopg_pool import ConnectionPool

with open("pyproject.toml","rb") as f:
    config = tomllib.load(f)
pool = ConnectionPool(
    conninfo=(config["database"]["DATABASE_URL"]),
    min_size=1,
    max_size=10
)