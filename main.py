from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from . import models
from . import database_interface
from . import database
import logging
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("apiserver")

app = FastAPI()

@app.on_event('startup')
def on_startup():
    database.create_db_and_tables()
    logger.info("Finished starting up!")

@app.get('/polls')
def getPolls(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)) -> list[models.PollRead]:
    polls = database_interface.read_polls(db, limit, offset)
    logger.info("Returning this value from GET polls:")
    logger.info(polls)
    logger.info("Choices:")
    if len(polls) > 0:
        logger.info(polls[0].choices)
    logger.info("Returning now.")
    return polls

@app.get('/polls/{pollId}')
def getPoll(pollId: int, db: Session = Depends(database.get_db)) -> models.PollRead:
    return database_interface.read_poll(db, pollId)

@app.get('/votes/{pollId}')
def getVotes(pollId: int, db: Session = Depends(database.get_db)) -> models.VoteSummary:
    votes = database_interface.read_votes(db, pollId)
    choiceSummaries = database_interface.read_vote_summary_choices(db, pollId)
    logger.info("Got votes:")
    logger.info(votes)
    logger.info("Got choice summaries:")
    logger.info(choiceSummaries)
    if len(choiceSummaries) == 0:
        poll = database_interface.read_poll(db, pollId)
        for choice in poll.choices:
            choiceSummaries.append(models.VoteSummaryChoices(choice=choice, total_votes=0))
    voteSummary = models.VoteSummary(choices=choiceSummaries, votes=votes)
    logger.info("Returning with this voteSummary:")
    logger.info(voteSummary)
    return voteSummary

@app.post('/polls')
def createPoll(poll: models.PollCreate, db: Session = Depends(database.get_db)) -> models.PollRead:
    poll = database_interface.create_poll(db, poll)
    logger.info("Returning this value from POST polls:")
    logger.info(poll)
    logger.info("Returning now.")
    return poll

@app.post('/votes/{pollId}')
def createVote(pollId: int, choice: models.VoteBase, db: Session = Depends(database.get_db)) -> models.VoteSummary:
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