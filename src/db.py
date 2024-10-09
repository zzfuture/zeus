from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def client():
    supabase = create_client(url, key)
    return supabase