# import os, json, time, random, requests
# from datetime import datetime, timedelta
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
# from jose import jwt, JWTError
# from pydantic import BaseModel
# import motor.motor_asyncio
# from dotenv import load_dotenv
# from fastapi.concurrency import run_in_threadpool

# # Import AI + utility modules
# from doctor_agent import doctor_reply
# from symptom_extractor import extract_structured
# from triage_engine import evaluate_triage
# from guideline_verifier import verify
# from utils import log_session

# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # you can replace "*" with ["http://localhost:5173"] if using Vite
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ----------------------------------------
# # Setup
# # ----------------------------------------
# load_dotenv()
# app.mount("/static", StaticFiles(directory="static"), name="static")

# SESSIONS = {}
# message_logs=[]
# # MongoDB setup
# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
# db = client["carecompanion"]
# users = db["users"]

# # JWT + Password hashing
# SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
# ALGORITHM = os.getenv("ALGORITHM", "HS256")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# # ----------------------------------------
# # Auth helper functions
# # ----------------------------------------
# def hash_password(password: str): return pwd_context.hash(password)
# def verify_password(password, hashed): return pwd_context.verify(password, hashed)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         user = await users.find_one({"email": email})
#         if not user:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# # ----------------------------------------
# # Models
# # ----------------------------------------
# class User(BaseModel):
#     email: str
#     password: str

# class ChatRequest(BaseModel):
#     session_id: str
#     message: str


# # ----------------------------------------
# # Auth routes
# # ----------------------------------------
# @app.post("/register")
# async def register(user: User):
#     if await users.find_one({"email": user.email}):
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_pw = hash_password(user.password)
#     await users.insert_one({"email": user.email, "password": hashed_pw})
#     return {"message": "User registered successfully"}

# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await users.find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token({"sub": user["email"]})
#     return {"access_token": token, "token_type": "bearer"}


# # ----------------------------------------
# # Static pages
# # ----------------------------------------
# @app.get("/")
# def serve_home():
#     return FileResponse(os.path.join("static", "login.html"))

# @app.get("/chat")
# def serve_chat():
#     return FileResponse(os.path.join("static", "index.html"))


# # ----------------------------------------
# # Chat route (✅ fully fixed)
# # ----------------------------------------

# @app.post("/api/chat")
# async def chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
#     global message_logs
#     sid = req.session_id

#     if sid not in SESSIONS:
#         SESSIONS[sid] = []
#         message_logs.clear()

#     # Store patient message
#     user_message = {"role": "patient", "message": req.message}
#     SESSIONS[sid].append({"role": "user", "content": req.message})
#     message_logs.append(user_message)

#     # -------------------------
#     # Doctor Response Handling
#     # -------------------------
#     try:
#         result = await run_in_threadpool(doctor_reply, SESSIONS[sid])
#         if isinstance(result, tuple):
#             reply, severity_flag = result
#         else:
#             reply, severity_flag = result, False
#     except Exception as e:
#         print(f"❌ Doctor agent error: {e}")
#         raise HTTPException(status_code=500, detail=f"Doctor agent error: {e}")

#     # Append to session
#     SESSIONS[sid].append({"role": "assistant", "content": reply})
#     message_logs.append({"role": "doctor", "message": reply})

#     # -------------------------
#     # Structured data & triage
#     # -------------------------
#     conv_text = "\n".join([f"{m['role']}: {m.get('content', '')}" for m in SESSIONS[sid]])

#     try:
#         structured = await run_in_threadpool(extract_structured, conv_text)
#     except Exception:
#         structured = {}

#     try:
#         raw_triage = await run_in_threadpool(evaluate_triage, structured)
#     except Exception:
#         raw_triage = {"level": "Routine", "reason": "No red flags found; symptoms appear non-urgent."}

#     verified = verify(raw_triage, [])

#     # -------------------------
#     # Map triage level → color & label
#     # -------------------------
#     level = verified.get("level", "Routine")
#     reason = verified.get("reason", "No red flags found; symptoms appear non-urgent.")
#     triage_display = {
#         "Emergency": {"color": "#e63946", "status": "🔴 Emergency — Immediate care required!"},
#         "Urgent": {"color": "#ff8800", "status": "🟠 Urgent — Needs prompt medical attention."},
#         "Routine": {"color": "#2a9d8f", "status": "🟢 Routine — No red flags; symptoms appear non-urgent."},
#         "Normal": {"color": "#2a9d8f", "status": "🟢 Normal — Stable, no emergency detected."}
#     }

#     triage_info = {
#         "level": level,
#         "reason": reason,
#         "color": triage_display.get(level, {}).get("color", "#2a9d8f"),
#         "status": triage_display.get(level, {}).get("status", "🟢 Routine condition"),
#         "severity_flag": severity_flag
#     }

#     # -------------------------
#     # Save conversation log
#     # -------------------------
#     log_session(sid, {
#         "session": SESSIONS[sid],
#         "structured": structured,
#         "triage": triage_info,
#         "ts": time.time()
#     })

#     # Final response
#     return {
#         "reply": reply,
#         "triage": triage_info,
#         "structured": structured
#     }


# # ----------------------------------------
# # Patient Simulator
# # ----------------------------------------
# @app.get("/api/simulate_patient_chat")
# async def simulate_patient_chat():
#     try:
#         file_path = os.path.join(os.getcwd(), "data", "vignettes.json")
#         if not os.path.exists(file_path):
#             raise HTTPException(status_code=500, detail=f"File not found: {file_path}")

#         with open(file_path, "r", encoding="utf-8") as f:
#             vignettes = json.load(f)

#         if not isinstance(vignettes, list) or not vignettes:
#             raise HTTPException(status_code=500, detail="Invalid or empty JSON data")

#         patient = random.choice(vignettes)
#         name = patient.get("name", "Unknown")
#         complaint = patient.get("chief_complaint", "No complaint provided")
#         symptoms = ", ".join(patient.get("symptoms", []))
#         history = patient.get("history", "No history provided")

#         message_history = [
#             {"role": "patient", "message": complaint},
#             {"role": "doctor", "message": f"Can you describe your {symptoms} in a bit more detail?"}
#         ]
#         doctor_response = f"Based on your history ({history}), it seems mild. Please rest and monitor your condition."

#         global message_logs
#         message_logs.clear()
#         message_logs.extend(message_history)
#         message_logs.append({"role": "doctor", "message": doctor_response})

#         print(f"✅ Simulation success for {name}")
#         return {
#             "patient_name": name,
#             "message_history": message_history,
#             "doctor_reply": doctor_response
#         }
#     except Exception as e:
#         print(f"❌ Simulation error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # ----------------------------------------
# # Generate Summary (✅ works for both chat & simulator)
# # ----------------------------------------
# @app.post("/api/generate_summary")
# async def generate_summary_api(current_user: dict = Depends(get_current_user)):
#     global message_logs
#     if not message_logs or len(message_logs) < 2:
#         print("⚠ No conversation found yet.")
#         return {"summary": "No conversation found yet."}

#     try:
#         from summary_agent import generate_summary
#         print("🧠 Generating summary using summary_agent.py ...")
#         summary_text = generate_summary(message_logs)

#         summary_doc = {
#             "user_email": current_user["email"],
#             "timestamp": datetime.utcnow(),
#             "summary_text": summary_text,
#             "conversation": message_logs
#         }

#         print("🟢 Saving summary to MongoDB...")
#         result = await db["summaries"].insert_one(summary_doc)
#         print("✅ Summary inserted with ID:", result.inserted_id)

#         return {
#             "summary": summary_text,
#             "message": "✅ Summary saved successfully.",
#             "saved": True
#         }
#     except Exception as e:
#         print(f"❌ Summary generation error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# # ----------------------------------------
# # Generate Differential Diagnosis (Top 5)
# # ----------------------------------------
# @app.post("/api/generate_diagnosis")
# async def generate_differential_diagnosis_api(current_user: dict = Depends(get_current_user)):
#     global message_logs

#     # ✅ Check if we have conversation context
#     if not message_logs or len(message_logs) < 2:
#         print("⚠ No conversation found yet for diagnosis.")
#         return {"diagnosis": "⚠ Please have a conversation first before generating diagnosis."}

#     try:
#         from differential_diagnosis import generate_differential_diagnosis
#         print("🧩 Generating differential diagnosis using differential_diagnosis.py ...")
#         diagnosis_text = generate_differential_diagnosis(message_logs)

#         # ✅ Save to MongoDB
#         diagnosis_doc = {
#             "user_email": current_user["email"],
#             "timestamp": datetime.utcnow(),
#             "diagnosis_text": diagnosis_text,
#             "conversation": message_logs
#         }

#         print("🟢 Saving diagnosis to MongoDB...")
#         result = await db["diagnoses"].insert_one(diagnosis_doc)
#         print("✅ Diagnosis inserted with ID:", result.inserted_id)

#         # ✅ Return final structured response
#         return {
#             "diagnosis": diagnosis_text,
#             "message": "✅ Top 5 differential diagnoses generated successfully.",
#             "saved": True
#         }

#     except Exception as e:
#         print(f"❌ Differential diagnosis generation error: {e}")
#         raise HTTPException(status_code=500,detail=str(e))

import os, json, time, random, requests
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

# Import AI + utility modules
from doctor_agent import doctor_reply
from symptom_extractor import extract_structured
from triage_engine import evaluate_triage
from guideline_verifier import verify
from utils import log_session

# ----------------------------------------
# FastAPI Setup
# ----------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust for frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
app.mount("/static", StaticFiles(directory="static"), name="static")

SESSIONS = {}
message_logs = []

# ----------------------------------------
# MongoDB Setup
# ----------------------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["carecompanion"]
users = db["users"]
summaries = db["summaries"]  # ✅ Store summaries/chat history
diagnoses = db["diagnoses"]

# ----------------------------------------
# JWT & Password Hashing
# ----------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str): return pwd_context.hash(password)
def verify_password(password, hashed): return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------------------------------
# Pydantic Models
# ----------------------------------------
class User(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

# ----------------------------------------
# Authentication Routes
# ----------------------------------------
@app.post("/register")
async def register(user: User):
    if await users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    await users.insert_one({"email": user.email, "password": hashed_pw})
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

# ----------------------------------------
# Static Pages
# ----------------------------------------
@app.get("/")
def serve_home():
    return FileResponse(os.path.join("static", "login.html"))

@app.get("/chat")
def serve_chat():
    return FileResponse(os.path.join("static", "index.html"))

# ----------------------------------------
# Main Chat API
# ----------------------------------------
@app.post("/api/chat")
async def chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    global message_logs
    sid = req.session_id

    if sid not in SESSIONS:
        SESSIONS[sid] = []
        message_logs.clear()

    # Store patient message
    user_message = {"role": "patient", "message": req.message}
    SESSIONS[sid].append({"role": "user", "content": req.message})
    message_logs.append(user_message)

    try:
        result = await run_in_threadpool(doctor_reply, SESSIONS[sid])
        reply, severity_flag = result if isinstance(result, tuple) else (result, False)
    except Exception as e:
        print(f"❌ Doctor agent error: {e}")
        raise HTTPException(status_code=500, detail=f"Doctor agent error: {e}")

    SESSIONS[sid].append({"role": "assistant", "content": reply})
    message_logs.append({"role": "doctor", "message": reply})

    # Extract structure & triage
    conv_text = "\n".join([f"{m['role']}: {m.get('content', '')}" for m in SESSIONS[sid]])
    structured = await run_in_threadpool(extract_structured, conv_text)
    raw_triage = await run_in_threadpool(evaluate_triage, structured)
    verified = verify(raw_triage, [])

    triage_display = {
        "Emergency": {"color": "#e63946", "status": "🔴 Emergency — Immediate care required!"},
        "Urgent": {"color": "#ff8800", "status": "🟠 Urgent — Needs prompt medical attention."},
        "Routine": {"color": "#2a9d8f", "status": "🟢 Routine — Non-urgent."},
        "Normal": {"color": "#2a9d8f", "status": "🟢 Normal — Stable condition."}
    }

    level = verified.get("level", "Routine")
    triage_info = {
        "level": level,
        "reason": verified.get("reason", "No red flags found."),
        "color": triage_display.get(level, {}).get("color", "#2a9d8f"),
        "status": triage_display.get(level, {}).get("status", "🟢 Routine condition"),
        "severity_flag": severity_flag
    }

    log_session(sid, {"session": SESSIONS[sid], "structured": structured, "triage": triage_info, "ts": time.time()})

    return {"reply": reply, "triage": triage_info, "structured": structured}

# ----------------------------------------
# Chat History APIs (NEW ✅)
# ----------------------------------------

@app.get("/api/summaries")
async def get_user_summaries(current_user: dict = Depends(get_current_user)):
    """Fetch all summaries for the logged-in user"""
    email = current_user["email"]
    cursor = summaries.find({"user_email": email}).sort("timestamp", -1)
    history = []
    async for doc in cursor:
        history.append({
            "_id": str(doc["_id"]),
            "summary_text": doc.get("summary_text", "No summary"),
            "timestamp": doc.get("timestamp")
        })
    return {"history": history}

@app.get("/api/summaries/{summary_id}")
async def get_single_summary(summary_id: str, current_user: dict = Depends(get_current_user)):
    """Fetch one summary with its conversation"""
    from bson import ObjectId
    doc = await summaries.find_one({"_id": ObjectId(summary_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Summary not found")
    doc["_id"] = str(doc["_id"])
    return doc

# ----------------------------------------
# Patient Simulator
# ----------------------------------------
@app.get("/api/simulate_patient_chat")
async def simulate_patient_chat():
    try:
        file_path = os.path.join(os.getcwd(), "data", "vignettes.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail=f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            vignettes = json.load(f)

        patient = random.choice(vignettes)
        message_history = [
            {"role": "patient", "message": patient.get("chief_complaint", "")},
            {"role": "doctor", "message": f"Can you describe your {', '.join(patient.get('symptoms', []))}?"}
        ]
        doctor_response = f"Based on your history ({patient.get('history', 'No history')}), please monitor and rest."

        global message_logs
        message_logs.clear()
        message_logs.extend(message_history)
        message_logs.append({"role": "doctor", "message": doctor_response})

        return {"patient_name": patient.get("name", "Unknown"), "message_history": message_history, "doctor_reply": doctor_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------
# Generate Summary + Save (✅)
# ----------------------------------------
@app.post("/api/generate_summary")
async def generate_summary_api(current_user: dict = Depends(get_current_user)):
    global message_logs
    if not message_logs or len(message_logs) < 2:
        return {"summary": "No conversation found yet."}

    try:
        from summary_agent import generate_summary
        summary_text = generate_summary(message_logs)

        summary_doc = {
            "user_email": current_user["email"],
            "timestamp": datetime.utcnow(),
            "summary_text": summary_text,
            "conversation": message_logs
        }
        result = await summaries.insert_one(summary_doc)
        return {"summary": summary_text, "saved": True, "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------------------
# Differential Diagnosis
# ----------------------------------------
@app.post("/api/generate_diagnosis")
async def generate_differential_diagnosis_api(current_user: dict = Depends(get_current_user)):
    global message_logs
    if not message_logs or len(message_logs) < 2:
        return {"diagnosis": "⚠ Please have a conversation first."}
    try:
        from differential_diagnosis import generate_differential_diagnosis
        diagnosis_text = generate_differential_diagnosis(message_logs)
        diagnosis_doc = {
            "user_email": current_user["email"],
            "timestamp": datetime.utcnow(),
            "diagnosis_text": diagnosis_text,
            "conversation": message_logs
        }
        await diagnoses.insert_one(diagnosis_doc)
        return {"diagnosis": diagnosis_text, "saved": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
