from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, ConversationSession, Message
from schemas import ChatRequest, ChatResponse
from llm import get_llm_response

app = FastAPI()

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=request.username).first()
    if not user:
        user = User(username=request.username)
        db.add(user)
        db.commit()
        db.refresh(user)

    if request.conversation_id:
        session = db.query(ConversationSession).filter_by(id=request.conversation_id).first()
    else:
        session = ConversationSession(user_id=user.id)
        db.add(session)
        db.commit()
        db.refresh(session)

    user_msg = Message(session_id=session.id, sender="user", content=request.message)
    db.add(user_msg)
    db.commit()

    ai_response = get_llm_response(request.message)

    ai_msg = Message(session_id=session.id, sender="ai", content=ai_response)
    db.add(ai_msg)
    db.commit()

    return ChatResponse(conversation_id=session.id, response=ai_response)