from . import models
from sqlmodel import Session, select, func
from sqlalchemy import and_

import logging
logger = logging.getLogger("apiserver")
def create_poll(db: Session, pollData: models.PollCreate) -> models.Poll:
    # no idea why but the relationship of Poll.choices errors out on model_validate
    # so remove choices from the initial data
    # then add it back once the Poll is instantiated...
    derp = pollData.choices.copy()
    pollData.choices.clear()
    poll : models.Poll = models.Poll.model_validate(pollData)
    for choice in derp:
        poll.choices.append(models.Choice(text=choice))
    db.add(poll)
    db.commit()
    db.refresh(poll)
    return poll

def create_vote(db: Session, voteData: models.VoteBase) -> models.Vote:
    vote: models.Vote = models.Vote.model_validate(voteData)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote

def read_polls(db : Session, limit: int = 10, offset: int = 0) -> list[models.Poll]:
    polls = db.exec(select(models.Poll).offset(offset).limit(limit)).all()
    return polls

def read_poll_choices(db: Session, pollId: int) -> list[models.Choice]:
    choices = db.exec(select(models.Choice).where(models.Choice.poll_id == pollId)).all()
    return choices

def read_votes(db: Session, pollId: int, limit: int = 100, offset: int = 0) -> list[models.Vote]:
    votes = db.exec(select(models.Vote).where(models.Vote.poll_id == pollId).offset(offset).limit(limit)).all()
    return votes

def read_vote_summary_choices(db: Session, pollId: int) -> list[models.VoteSummaryChoices]:
    stmt = select(models.Choice, func.count(models.Vote.choice_id)).join(models.Vote, isouter=True).where((models.Choice.poll_id == pollId)).group_by(models.Choice.choice_id)
    votes = db.exec(stmt).all()
    voteSummaries: list[models.VoteSummaryChoices] = []
    for choice, cnt in votes:
        voteSummaries.append(models.VoteSummaryChoices(choice=choice, total_votes=cnt))
    return voteSummaries

def read_poll(db: Session, pollId: int) -> models.Poll:
    poll = db.exec(select(models.Poll).where(models.Poll.poll_id == pollId)).one_or_none()
    return poll