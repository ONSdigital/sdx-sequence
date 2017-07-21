from sqlalchemy import create_engine
import testing.postgresql

import settings
from sequences import create_sequences

# Launch new PostgreSQL server
Postgres = testing.postgresql.PostgresqlFactory(cache_initialized_db=False)
postgresql = Postgres()
settings.DB_URL = postgresql.url()
engine = create_engine(postgresql.url())
create_sequences(engine)
