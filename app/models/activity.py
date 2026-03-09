from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    level = Column(Integer, nullable=False, default=1)

    parent = relationship("Activity", remote_side=[id])
    children = relationship("Activity", back_populates="parent")
    organizations = relationship("Organization", secondary="organization_activities", back_populates="activities")