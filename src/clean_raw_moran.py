"""
A script to clean the raw data

NOTE this script consider P1 v P2 and the same match as P2 v P1 and calculates
the fixation probabilities by considering both match ups. This holds if the
Moran process data is generated using N / 2 individuals of the first type in a
population of size N.
"""
import pandas as pd
import csv


# Read in the player representations
with open("../data/players.csv", "r") as f:
    reader = csv.reader(f)
    index_to_players = {row[0]: row[1] for row in reader}

# Read in the data
data = []
for N in range(2, 14 + 1, 2):
    for noise, filename in enumerate(["../data/sims_{}.csv".format(N),
                                 "../data/noise_sims_{0:02d}.csv".format(N)]):
        noise = bool(noise)

        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:

                index1, index2, indexwinner, winnercount = row

                p1 = index_to_players[index1]
                p2 = index_to_players[index2]
                winner = index_to_players[indexwinner]

                if str(p1) > str(p2):
                    p1, p2 = p2, p1

                data.append([noise, int(N), p1, p2, winner, int(winnercount)])

full_data = pd.DataFrame(data, columns=["Noise", "N", "P1", "P2",
                                        "Winner", "Winner count"])

# Clean and write the data to file.
with open("../data/sims_summary.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["P1", "P2", "N", "Noise",
                     "Repetitions", "P1 fixation", "P2 fixation"])
    for players_n_noise, df in full_data.groupby(["P1", "P2", "N", "Noise"]):

        total = df["Winner count"].sum()

        fixation_probabilities = []
        for i in range(2):
            count = float(df[df["Winner"] == players_n_noise[i]]["Winner count"].sum())
            fixation_probabilities.append(count / total)

        writer.writerow([*players_n_noise, total, *fixation_probabilities])