import os
# set these before importing server to stop the process exiting due to them being missing
os.environ['POSTGRES_HOST'] = os.getenv("POSTGRES_HOST", "127.0.0.1")
os.environ['POSTGRES_PORT'] = os.getenv("POSTGRES_PORT", "5432")
os.environ['POSTGRES_NAME'] = os.getenv("POSTGRES_NAME", "sdx")
os.environ['POSTGRES_USER'] = os.getenv("POSTGRES_USER", "sdx")
os.environ['POSTGRES_PASSWORD'] = os.getenv("POSTGRES_PASSWORD", "sdx")
