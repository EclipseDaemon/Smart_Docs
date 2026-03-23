from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.db.base import Base, TimeStampMixin


class Document(Base, TimeStampMixin):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_type = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    search_vector = Column(TSVECTOR, nullable=True)
    is_processed = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="documents")