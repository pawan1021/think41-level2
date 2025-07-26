from database import Base, engine
import models 

print("📦 Creating tables using engine:", engine)

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")

