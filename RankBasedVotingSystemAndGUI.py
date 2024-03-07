import customtkinter
from ElectionLogic import Election
import customtkinter as ctk
from matplotlib.figure import Figure #source - https://www.geeksforgeeks.org/matplotlib-tutorial/#
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #source- https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
#Source: https://matplotlib.org/stable/users/explain/figure/backends.html
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")
class ElectionGUI(ctk.CTk):
    """
    This entire class is where the magic happens! This creates all GUI elements, allows for user interaction, and send user inputs
    to the election logic class. This information is returned with Get_results and displayed in our GUI!
    """
    def __init__(self):
        """
        We initialize every principle of the GUI we wanted to design, and we call super() to retrieve the properties of CTK)
        """
        super().__init__()

        # Creating the Title and the Window
        self.title("Election System")
        self.geometry("1000x1000")

        # Title of the GUI
        self.title_label = customtkinter.CTkLabel(self, text="Rank Based Voting System",
        font=customtkinter.CTkFont(size=50, weight="bold"))
        self.title_label.place(x=200, y=10)

        # Connecting the Election class to the GUI
        self.election = Election()

        # Candidate Entry and Submit Button
        self.candidate_entry = ctk.CTkEntry(self, width=580, placeholder_text="Enter candidate names here, separated by commas")
        self.candidate_entry.place(x=10, y=120)
        self.add_candidate_button = ctk.CTkButton(self, text="Add Candidates", command=self.add_candidate)
        self.add_candidate_button.place(x=600, y=120)

        # Voter Entry and Submit Button
        self.voter_entry = ctk.CTkEntry(self, width=580, placeholder_text="Enter voter names here, separated by commas")
        self.voter_entry.place(x=10, y=160)
        self.register_voter_button = ctk.CTkButton(self, text="Register Voters", command=self.register_voter)
        self.register_voter_button.place(x=600, y=160)

        # The Actual Voting/Ranking and Submit Button
        self.voting_voter_entry = ctk.CTkEntry(self, width=580, placeholder_text="Enter the name of the current voter")
        self.voting_voter_entry.place(x=10, y=200)
        self.rankings_entry = ctk.CTkEntry(self, width=580, placeholder_text="Enter candidate names in order separated by commas")
        self.rankings_entry.place(x=10, y=240)
        self.cast_vote_button = ctk.CTkButton(self, text="Cast Vote", command=self.cast_vote)
        self.cast_vote_button.place(x=600, y=240)

################################ Displaying Candidates on GUI
        # title for the candidate display
        self.candidate_display_title = ctk.CTkLabel(self, text="List of Candidates")
        self.candidate_display_title.place(x=750, y=90)

        self.candidate_display_width = 200
        self.candidate_display_height = 300
        self.candidate_display_x = 750
        self.candidate_display_y = 120

        self.candidate_display = ctk.CTkTextbox(self, width=self.candidate_display_width, height=self.candidate_display_height, state='disabled')
        self.candidate_display.place(x=self.candidate_display_x, y=self.candidate_display_y)

################################ Displaying Voters on GUI
        # title for the voter display
        self.voter_display_title = ctk.CTkLabel(self, text="List of Voters")
        self.voter_display_title.place(x=750, y=420)

        self.voter_display_width = 200
        self.voter_display_height = 300
        self.voter_display_x = 750
        self.voter_display_y = 450

        self.voter_display = ctk.CTkTextbox(self, width=self.voter_display_width, height=self.voter_display_height, state='disabled')
        self.voter_display.place(x=self.voter_display_x, y=self.voter_display_y)
################################################################
        # Display results
        self.results_display = ctk.CTkTextbox(self, width=580, height=100, state='disabled')
        self.results_display.place(x=10, y=310)
        # Button to Show Results
        self.show_results_button = ctk.CTkButton(self, text="Show Results", command=self.display_results)
        self.show_results_button.place(x=600, y=310)
        # The spot where the MatPLotLib graph will be displayed
        self.canvas_location = ctk.CTkFrame(self, width=580, height=300)
        self.canvas_location.place(x=10, y=450)

    def add_candidate(self):
        candidate_names = self.candidate_entry.get().split(',')
        try:
            self.election.add_candidates([name.strip() for name in candidate_names])
            print("Candidates added successfully.")
            self.update_candidate_display()
        except Exception as e:
            print(f"Error adding candidates: {e}")
        self.candidate_entry.delete(0, 'end')
    def update_candidate_display(self):
        self.candidate_display.configure(state='normal')
        self.candidate_display.delete("1.0", "end")

        # Updates the display with the new list of candidates
        candidate_names = [candidate.name for candidate in self.election.candidates]
        self.candidate_display.insert("1.0", "\n".join(candidate_names))

        self.candidate_display.configure(state='disabled')

    def update_voter_display(self):
        self.voter_display.configure(state='normal')
        self.voter_display.delete("1.0", "end")

        # Updates the display with the new list of voters
        voter_names = [voter.voter_name for voter in self.election.voters.values()]
        self.voter_display.insert("1.0", "\n".join(voter_names))

        self.voter_display.configure(state='disabled')
    def register_voter(self):
        voter_names = self.voter_entry.get().split(',')
        try:
            self.election.register_voters([name.strip() for name in voter_names])
            print("Voters registered successfully.")
            self.update_voter_display()
        except Exception as e:
            print(f"Error registering voters: {e}")
        self.voter_entry.delete(0, 'end')

    def cast_vote(self):
        voter_name = self.voting_voter_entry.get().strip()
        rankings = self.rankings_entry.get().split(',')
        try:
            self.election.cast_vote(voter_name, [rank.strip() for rank in rankings])
            print(f"Vote cast successfully for voter {voter_name}.")
        except Exception as e:
            print(f"Error casting vote: {e}")
        self.voting_voter_entry.delete(0, 'end')
        self.rankings_entry.delete(0, 'end')

    def display_results(self):
        try:
            results = self.election.get_results()
            self.results_display.configure(state='normal')
            self.results_display.delete("1.0", "end")
            self.results_display.insert("1.0", results)
            self.results_display.configure(state='disabled')
            self.display_graph()

        except Exception as e:
            print(f"Error displaying results: {e}")

    ##########################Plotting Results with Matplotlib######################################
    def display_graph(self):

        # Taking the results and plotting them with Matplotlib
        sorted_candidates = sorted(self.election.candidates, key=lambda c: c.points, reverse=True)
        names = [candidate.name.title() for candidate in sorted_candidates]
        points = [candidate.points for candidate in sorted_candidates]

        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot(111)
        ax.bar(names, points, color='blue')
        ax.set_title('Election Results')
        ax.set_xlabel('Candidates')
        ax.set_ylabel('Points')

        # Places the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_location)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()

if __name__ == "__main__":
    GUI = ElectionGUI()
    GUI.mainloop()
