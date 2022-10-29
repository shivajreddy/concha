"""
SQLAlchemy models representing PSQL tables
"""

from server.database import Base

from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_data"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    image = Column(String, nullable=False)

    def __repr__(self):
        return f"<User #{self.id}: {self.name} {self.email}>"


class AudioData(Base):
    __tablename__ = "audio_data"

    unique_id = Column(String, primary_key=True, nullable=False)
    session_id = Column(Integer, nullable=False)
    ticks = Column(ARRAY(Integer), nullable=False)
    selected_tick = Column(Integer, nullable=False)
    step_count = Column(Integer, nullable=False)

    # Relation to 'user' table
    user_id = Column(String, ForeignKey("user_data.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

    def __repr__(self):
        return f"<AudioData #{self.session_id} >"
