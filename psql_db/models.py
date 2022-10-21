"""
SQLAlchemy models representing PSQL tables
"""

from psql_db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ARRAY, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    image = Column(String, nullable=False)

    def __repr__(self):
        return f"<User #{self.id}: {self.name} {self.email}>"


class AudioDataFile(Base):
    __tablename__ = "audio_data"
    session_id = Column(Integer, primary_key=True, nullable=False)
    ticks = Column(ARRAY(Integer), nullable=False)
    selected_tick = Column(Integer, nullable=False)
    step_count = Column(Integer, nullable=False)

    # Relation to 'user' table
    # user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    # user = relationship("User")

    def __repr__(self):
        return f"<AudioDataFile #{self.session_id} >"
