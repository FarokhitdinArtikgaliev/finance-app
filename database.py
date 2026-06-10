import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://finance_user:unm4SB9TiYJzejHX5Ml1DENtdKZ2mJO5@dpg-d8kdekojs32c73em3740-a.oregon-postgres.render.com/finance_o60s"

def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor,
        sslmode="require"
    )