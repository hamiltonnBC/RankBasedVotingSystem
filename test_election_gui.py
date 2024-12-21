"""
Unit tests for the GUI components of the election system.
"""

import unittest
from unittest.mock import MagicMock, patch
from RankBasedVotingSystemAndGUI import ElectionGUI

class TestElectionGUI(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.gui = ElectionGUI()

    def tearDown(self):
        """Clean up after each test"""
        self.gui.destroy()

    def test_add_candidate(self):
        """Test adding candidates through the GUI"""
        self.gui.candidate_entry.insert(0, "Alice, Bob, Charlie")
        self.gui.add_candidate()

        # Verify candidates were added
        candidate_names = [c.name for c in self.gui.election.candidates]
        self.assertEqual(candidate_names, ["alice", "bob", "charlie"])

        # Verify entry was cleared
        self.assertEqual(self.gui.candidate_entry.get(), "")

    def test_register_voter(self):
        """Test registering voters through the GUI"""
        self.gui.voter_entry.insert(0, "voter1, voter2")
        self.gui.register_voter()

        # Verify voters were registered
        self.assertTrue("voter1" in self.gui.election.voters)
        self.assertTrue("voter2" in self.gui.election.voters)

        # Verify entry was cleared
        self.assertEqual(self.gui.voter_entry.get(), "")

    def test_cast_vote(self):
        """Test casting a vote through the GUI"""
        # First add candidates and register voter
        self.gui.election.add_candidates(["alice", "bob", "charlie"])
        self.gui.election.register_voters(["voter1"])

        # Cast vote
        self.gui.voting_voter_entry.insert(0, "voter1")
        self.gui.rankings_entry.insert(0, "alice, bob, charlie")
        self.gui.cast_vote()

        # Verify vote was recorded
        self.assertTrue(self.gui.election.voters["voter1"].has_voted)

        # Verify entries were cleared
        self.assertEqual(self.gui.voting_voter_entry.get(), "")
        self.assertEqual(self.gui.rankings_entry.get(), "")

    @patch('matplotlib.figure.Figure')
    @patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg')
    def test_display_results(self, mock_canvas, mock_figure):
        """Test displaying results and graph"""
        # Setup mock election results
        self.gui.election.add_candidates(["alice", "bob"])
        self.gui.election.register_voters(["voter1"])
        self.gui.election.cast_vote("voter1", ["alice", "bob"])

        # Test display_results method
        self.gui.display_results()

        # Verify results were displayed
        results_text = self.gui.results_display.get("1.0", "end-1c")
        self.assertIn("alice", results_text.lower())
        self.assertIn("points", results_text.lower())

        # Verify graph was created
        mock_figure.assert_called()
        mock_canvas.assert_called()

    def test_update_displays(self):
        """Test updating candidate and voter displays"""
        # Add candidates and voters
        self.gui.election.add_candidates(["alice", "bob"])
        self.gui.election.register_voters(["voter1"])

        # Update displays
        self.gui.update_candidate_display()
        self.gui.update_voter_display()

        # Verify candidate display
        candidate_text = self.gui.candidate_display.get("1.0", "end-1c")
        self.assertIn("alice", candidate_text.lower())
        self.assertIn("bob", candidate_text.lower())

        # Verify voter display
        voter_text = self.gui.voter_display.get("1.0", "end-1c")
        self.assertIn("voter1", voter_text.lower())

if __name__ == '__main__':
    unittest.main()