from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BaseRestaurant:
    id: int
    name: str


@dataclass
class Restaurant(BaseRestaurant):
    score: int
    voters: int


@dataclass
class TodayPollResponse:
    top: Restaurant
    rankings: List[Restaurant]
    available_votes: int


@dataclass
class VoteResponseResponse(TodayPollResponse):
    error: Optional[str]


@dataclass
class PollHistoryResponse:
    date: str
    restaurant: BaseRestaurant
