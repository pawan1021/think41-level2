from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

from pydantic import BaseModel
from datetime import datetime
import uuid

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    conversation_id: str
    user_message: str
    ai_response: str

# POST /api/chat
@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if request.conversation_id:
        session = db.query(models.ConversationSession).filter_by(id=request.conversation_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Conversation session not found")
    else:
        session = models.ConversationSession(id=str(uuid.uuid4()), user_id=request.user_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = models.Message(
        session_id=session.id,
        sender="user",
        content=request.message,
        timestamp=datetime.utcnow()
    )
    db.add(user_msg)

    # Placeholder AI logic
    ai_text = f"This is a placeholder response to: '{request.message}'"

    # Save AI response
    ai_msg = models.Message(
        session_id=session.id,
        sender="ai",
        content=ai_text,
        timestamp=datetime.utcnow()
    )
    db.add(ai_msg)
    db.commit()

    return {
    "conversation_id": session_id,
    "user_message": message.message,
    "ai_response": ai_response
}

