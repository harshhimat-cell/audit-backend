from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from routers import auth, waitlist, vault, rewards, admin
except ImportError:
    import auth as auth
    import waitlist as waitlist
    import vault as vault
    import rewards as rewards
    import admin as admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AuBit API",
    description="Backend for AuBit — the debit card that earns real assets",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/auth",     tags=["Auth"])
app.include_router(waitlist.router,  prefix="/waitlist", tags=["Waitlist"])
app.include_router(vault.router,     prefix="/vault",    tags=["Vault"])
app.include_router(rewards.router,   prefix="/rewards",  tags=["Rewards"])
app.include_router(admin.router,     prefix="/admin",    tags=["Admin"])

@app.get("/")
def root():
    return {"status": "AuBit API is live", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
