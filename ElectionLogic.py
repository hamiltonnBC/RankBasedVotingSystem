from dataclasses import dataclass
from typing import List, Dict
@dataclass
class Candidate:
    """
    Dataclass representing each candidate. The init method is provided on account of it being a dataclass. Stores name and points.
    """
    name: str
    points: int = 0  # Initialize candidate points to 0
@dataclass
class Voter:
    """
    Dataclass representing each voter. The init method is provided on account of it being a dataclass. Stores names and if they have voted yet.
    """
    voter_name: str
    has_voted: bool = False  # To keep track if the voter has already voted
class Election:
    """
    Class representing the election. It holds a list of candidates and a dictionary of voters, to hold the
    name of the voter and their selections.
    """
    def __init__(self):
        self.candidates: List[Candidate] = []
        self.voters: Dict[str, Voter] = {}


##########################Adding candidates section######################################

    def add_candidates(self, candidate_names: List[str]):
        """
        Add candidates to the list of candidates. Receieves a cleaned list from GUI.
        """
        for name in candidate_names:
            cleaned_name = name.strip().lower()
            self.candidates.append(Candidate(cleaned_name))

    #########################Adding Voters section#######################################
    def register_voters(self, voter_names: List[str]):
        """
        Add voters to the list of voters. Receives a list from GUI.
        """
        for voter_name in voter_names:
            if voter_name in self.voters:
                raise Exception("Voter already registered.")
            self.voters[voter_name] = Voter(voter_name)

###casting votes and adding amounts section#######################################
    def cast_votes(self, votes: Dict[str, List[str]]):
        """
        unused, useful if we wanted to process multiple votes at the same time
        """
        for voter_name, rankings in votes.items():
            self.cast_vote(voter_name, rankings)

    def cast_vote(self, voter_name: str, rankings: List[str]):
        """
        Uses each voter's rankings to add points to each candidate, and mark the voter as having voted.
        :param voter_name:
        :param rankings:
        :return: Added points to each candidate
        """

        if voter_name not in self.voters:
            raise Exception("Voter not registered.")
        if self.voters[voter_name].has_voted:
            raise Exception("Voter has already voted.")
        # Assign points based on rankings
        points_for_rank = len(self.candidates) - 1
        for candidate_name in rankings:
            for candidate in self.candidates:
                if candidate.name == candidate_name:
                    candidate.points += points_for_rank
                    points_for_rank -= 1  # Decrease points for the next rank
        # Mark the voter as having voted
        self.voters[voter_name].has_voted = True

    #########################Finding results#######################################
    def get_results(self):
        """
        method sorts the list of candidates by points, and returns the winner.
        :return: winner
        """
        sorted_candidates = sorted(self.candidates, key=lambda c: c.points, reverse=True) #https://stackoverflow.com/questions/8966538/syntax-behind-sortedkey-lambda
        # sorted sorts from least to most, so reverse=True to display winner first
        results = "\n".join([f"{candidate.name} - Points: {candidate.points}" for candidate in sorted_candidates])
        winner = sorted_candidates[0].name if sorted_candidates else "No candidates"
        print(results + f"\nThe winner of the election is: {winner}!")
        return results + f"\nThe winner of the election is: {winner}!"