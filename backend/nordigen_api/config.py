import asyncio
import os
import uuid

from dotenv import load_dotenv

load_dotenv()

nordigen_secret_id = os.getenv("NORDIGEN_SECRET_ID")
nordigen_secret_key = os.getenv("NORDIGEN_SECRET_KEY")
hardcoded_user_id = uuid.UUID("91683e5e-447a-4ffa-93be-4106db32de97")
institution_connected_url_path = "connected"
backend_url = os.getenv("BACKEND_URL")
frontend_url = os.getenv("FRONTEND_URL")

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
