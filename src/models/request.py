from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    response = Column(String, nullable=True)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="requests")

    def __repr__(self):
        return f"<Request id={self.id} model={self.model} prompt='{self.prompt[:20]}...' status={self.status}>"