from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlmodel import Session, select, text
from . import models
from . import database_interface
from . import database
import logging
from sqlalchemy.exc import IntegrityError, OperationalError
import os
import signal
import sys

logger = logging.getLogger("apiserver")

app = FastAPI()

@app.on_event('startup')
def on_startup():
    try:
        database.create_db_and_tables()
        logger.info("Finished starting up!")
    except OperationalError as oe:
        logger.error(oe)
        logger.error("Attempting to exit by sending SIGTERM to pid {}".format(os.getpid()))
        os.kill(os.getpid(), signal.SIGTERM)
        sys.exit(4)
        return

@app.get('/healthcheck')
async def getHealthCheck(response: Response) -> models.HealthCheck:
    try:
        with Session(database.get_engine()) as db:
            db.exec(text('SELECT 1;'))
            db.commit()
            return models.HealthCheck(message="healthy")
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        errorMsg = str(e)
        return models.HealthCheck(message=errorMsg)

@app.get('/polls')
async def getPolls(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)) -> list[models.PollRead]:
    polls = database_interface.read_polls(db, limit, offset)
    return polls

@app.get('/polls/{pollId}')
async def getPoll(pollId: int, db: Session = Depends(database.get_db)) -> models.PollRead:
    return database_interface.read_poll(db, pollId)

@app.get('/votes/{pollId}')
async def getVotes(pollId: int, db: Session = Depends(database.get_db)) -> models.VoteSummary:
    votes = database_interface.read_votes(db, pollId)
    choiceSummaries = database_interface.read_vote_summary_choices(db, pollId)
    if len(choiceSummaries) == 0:
        poll = database_interface.read_poll(db, pollId)
        for choice in poll.choices:
            choiceSummaries.append(models.VoteSummaryChoices(choice=choice, total_votes=0))
    voteSummary = models.VoteSummary(choices=choiceSummaries, votes=votes)
    return voteSummary

@app.post('/polls')
async def createPoll(poll: models.PollCreate, db: Session = Depends(database.get_db)) -> models.PollRead:
    poll = database_interface.create_poll(db, poll)
    return poll

@app.post('/votes/{pollId}')
async def createVote(pollId: int, choice: models.VoteBase, db: Session = Depends(database.get_db)) -> models.VoteSummary:
    try:
        vote = database_interface.create_vote(db, choice)
    except IntegrityError as e:
        if 'Duplicate entry' in e.args[0]:
            logger.info("User tried voting twice! Ban them!")
            raise HTTPException(status_code=400, detail="You have already voted on this poll")
    votes = database_interface.read_votes(db, pollId)
    choiceSummaries = database_interface.read_vote_summary_choices(db, pollId)
    if len(choiceSummaries) == 0:
        poll = database_interface.read_poll(db, pollId)
        for pollChoice in poll.choices:
            choiceSummaries.append(models.VoteSummaryChoices(choice=pollChoice, total_votes=0))
    voteSummary = models.VoteSummary(choices=choiceSummaries, votes=votes)
    return voteSummary