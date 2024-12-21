"""
Unit tests for the core election system logic.
"""

import unittest
from ElectionLogic import Election, Candidate, Voter


class TestElectionSystem(unittest.TestCase):
    def setUp(self):
        """Set up a new election instance before each test"""
        self.election = Election()

    def test_add_candidates(self):
        """Test adding candidates to the election"""
        candidate_names = ["Alice", " Bob ", "  Charlie  "]
        self.election.add_candidates(candidate_names)

        self.assertEqual(len(self.election.candidates), 3)
        self.assertEqual(self.election.candidates[0].name, "alice")
        self.assertEqual(self.election.candidates[1].name, "bob")
        self.assertEqual(self.election.candidates[2].name, "charlie")

    def test_register_voters(self):
        """Test registering voters"""
        voter_names = ["voter1", "voter2"]
        self.election.register_voters(voter_names)

        self.assertEqual(len(self.election.voters), 2)
        self.assertIn("voter1", self.election.voters)
        self.assertFalse(self.election.voters["voter1"].has_voted)

    def test_register_duplicate_voter(self):
        """Test that registering a duplicate voter raises an exception"""
        self.election.register_voters(["voter1"])

        with self.assertRaises(Exception) as context:
            self.election.register_voters(["voter1"])
        self.assertTrue("Voter already registered" in str(context.exception))

    def test_cast_vote(self):
        """Test casting a single vote"""
        self.election.add_candidates(["alice", "bob", "charlie"])
        self.election.register_voters(["voter1"])

        rankings = ["alice", "bob", "charlie"]
        self.election.cast_vote("voter1", rankings)

        # Check points: first place gets 2 points, second gets 1, third gets 0
        for candidate in self.election.candidates:
            if candidate.name == "alice":
                self.assertEqual(candidate.points, 2)
            elif candidate.name == "bob":
                self.assertEqual(candidate.points, 1)
            elif candidate.name == "charlie":
                self.assertEqual(candidate.points, 0)

    def test_cast_vote_unregistered_voter(self):
        """Test that unregistered voters cannot vote"""
        self.election.add_candidates(["alice", "bob"])

        with self.assertRaises(Exception) as context:
            self.election.cast_vote("unregistered_voter", ["alice", "bob"])
        self.assertTrue("Voter not registered" in str(context.exception))

    def test_cast_vote_twice(self):
        """Test that voters cannot vote twice"""
        self.election.add_candidates(["alice", "bob"])
        self.election.register_voters(["voter1"])

        self.election.cast_vote("voter1", ["alice", "bob"])

        with self.assertRaises(Exception) as context:
            self.election.cast_vote("voter1", ["bob", "alice"])
        self.assertTrue("Voter has already voted" in str(context.exception))

    def test_get_results(self):
        """Test getting election results"""
        self.election.add_candidates(["alice", "bob", "charlie"])
        self.election.register_voters(["voter1", "voter2"])

        # First voter ranks: alice > bob > charlie
        self.election.cast_vote("voter1", ["alice", "bob", "charlie"])
        # Second voter ranks: bob > alice > charlie
        self.election.cast_vote("voter2", ["bob", "alice", "charlie"])

        results = self.election.get_results()

        # Both alice and bob should have 3 points, charlie should have 0
        self.assertIn("alice - Points: 3", results)
        self.assertIn("bob - Points: 3", results)
        self.assertIn("charlie - Points: 0", results)


if __name__ == '__main__':
    unittest.main()