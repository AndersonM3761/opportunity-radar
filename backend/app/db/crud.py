from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from app.db import models
import json
import uuid

def get_or_create_user(db: Session, profile: dict) -> models.User:
    email = profile.get("email", "anonymous@test.com")
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        user = models.User(
            id=str(uuid.uuid4()),
            email=email,
            branch=profile.get("branch"),
            year=profile.get("year"),
            interests=json.dumps(profile.get("interests", [])),
            goal=profile.get("goal")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def upsert_opportunity(db: Session, opp_data: dict) -> models.Opportunity:
    # Basic SQLite upsert pattern
    stmt = insert(models.Opportunity).values(
        id=str(uuid.uuid4()),
        name=opp_data["name"],
        type=opp_data["type"].lower() if opp_data["type"].lower() in [e.value for e in models.OpportunityType] else "other",
        url=opp_data["link"],
        deadline=opp_data.get("deadline", ""),
        deadline_status="confirmed",
        verified_live=True
    )
    
    # On conflict (URL exists), just return the existing record without doing anything
    stmt = stmt.on_conflict_do_nothing(index_elements=['url'])
    db.execute(stmt)
    db.commit()
    
    # Retrieve it (whether just inserted or pre-existing)
    return db.query(models.Opportunity).filter(models.Opportunity.url == opp_data["link"]).first()

def link_user_opportunity(db: Session, user_id: str, opp_id: str, why_relevant: str):
    # Check if link exists
    link = db.query(models.UserOpportunity).filter(
        models.UserOpportunity.user_id == user_id,
        models.UserOpportunity.opportunity_id == opp_id
    ).first()
    
    if not link:
        link = models.UserOpportunity(
            id=str(uuid.uuid4()),
            user_id=user_id,
            opportunity_id=opp_id,
            why_relevant=why_relevant
        )
        db.add(link)
        db.commit()
