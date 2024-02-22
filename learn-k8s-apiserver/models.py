from sqlmodel import Field, Relationship, SQLModel, func
from typing import Optional, List
import datetime
from pydantic import BaseModel

class HealthCheck(BaseModel):
    message: str

class Choice(SQLModel, table=True):
    choice_id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: Optional[int] = Field(default=None, foreign_key="poll.poll_id")
    text: str

    poll: Optional["Poll"] = Relationship(back_populates="choices")

class ChoiceRead(SQLModel):
    choice_id: int
    poll_id: int
    text: str

class PollBase(SQLModel):
    title: str
    creator_id: str
    expiration_time: datetime.datetime
    short_description: str
    long_description: str

class PollCreate(PollBase):
    choices: list[str]

class Poll(PollBase, table=True):
    poll_id: Optional[int] = Field(default=None, primary_key=True)
    created_time: Optional[datetime.datetime] = Field(default=None, sa_column_kwargs={'server_default': func.now()})
    view_count: Optional[int] = Field(default=0)
    vote_count: Optional[int] = Field(default=0)
    
    choices: List["Choice"] = Relationship(back_populates="poll")
    votes: List["Vote"] = Relationship(back_populates="poll")

class PollRead(PollBase):
    poll_id: int
    created_time: datetime.datetime
    view_count: int
    vote_count: int
    choices: List[ChoiceRead]

class VoteBase(SQLModel):
    poll_id: Optional[int] = Field(default=None, foreign_key="poll.poll_id", primary_key=True)
    choice_id: Optional[int] = Field(default=None, foreign_key="choice.choice_id")
    user_id: Optional[str] = Field(default=None, primary_key=True)

class Vote(VoteBase, table=True):
    vote_time: Optional[datetime.datetime] = Field(default=None, sa_column_kwargs={'server_default': func.now()})
    poll: Optional["Poll"] = Relationship(back_populates="votes")
    choice: Optional["Choice"] = Relationship()

class VoteRead(VoteBase):
    poll_id: int
    choice_id: int
    user_id: str
    vote_time: datetime.datetime

class VoteSummaryChoices(SQLModel):
    choice: ChoiceRead
    total_votes: int

class VoteSummary(SQLModel):
    choices: list[VoteSummaryChoices]
    votes: list[VoteRead]