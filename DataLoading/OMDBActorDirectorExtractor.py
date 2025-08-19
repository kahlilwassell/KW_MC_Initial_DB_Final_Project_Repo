import csv
import time
import requests
import pandas as pd

API_KEY = "86c94666"
INPUT_FILE = "../Data/Entities/movies.csv"

OUT_ACTORS = "../Data/actors.csv"      # unique actor nodes
OUT_DIRECTORS = "../Data/directors.csv"  # unique director nodes
OUT_ACTS_IN = "../Data/actsIn.csv"      # relationships
OUT_DIRECTS = "../Data/directs.csv"     # relationships


def omdb(imdb_id):
    r = requests.get("https://www.omdbapi.com/", params={"i": imdb_id, "apikey": API_KEY})
    r.raise_for_status()
    return r.json()


# collect all rows for later deduplication
actor_edges = []
director_edges = []

with open(INPUT_FILE, encoding="utf-8") as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
        iid = row["movieId"].strip()
        try:
            j = omdb(iid)
            actors = [x.strip() for x in j.get("Actors", "").split(",") if x.strip()]
            directors = [x.strip() for x in j.get("Director", "").split(",") if x.strip()]

            for a in actors:
                actor_edges.append((iid, a))
            for d in directors:
                director_edges.append((iid, d))

            time.sleep(0.25)  # avoid hammering OMDb
        except Exception as e:
            print("skipping", iid, e)

# Build unique Actor list
actor_df = pd.DataFrame(actor_edges, columns=["imdbId", "name"])
unique_actors = actor_df["name"].drop_duplicates().sort_values(key=lambda s: s.str.casefold()).reset_index(drop=True)
actor_ids = pd.Series(range(1, len(unique_actors) + 1), index=unique_actors)
actors_table = pd.DataFrame({"actorId": actor_ids.values, "name": actor_ids.index})

# Build unique Director list
director_df = pd.DataFrame(director_edges, columns=["imdbId", "name"])
unique_directors = director_df["name"].drop_duplicates().sort_values(key=lambda s: s.str.casefold()).reset_index(drop=True)
director_ids = pd.Series(range(1, len(unique_directors) + 1), index=unique_directors)
directors_table = pd.DataFrame({"directorId": director_ids.values, "name": director_ids.index})

# Build edges with IDs
acts_in_edges = actor_df.assign(actorId=actor_df["name"].map(actor_ids))[["movieId", "actorId"]].drop_duplicates()
directs_edges = director_df.assign(directorId=director_df["name"].map(director_ids))[["movieId", "directorId"]].drop_duplicates()

# Save CSVs
actors_table.to_csv(OUT_ACTORS, index=False)
directors_table.to_csv(OUT_DIRECTORS, index=False)
acts_in_edges.to_csv(OUT_ACTS_IN, index=False)
directs_edges.to_csv(OUT_DIRECTS, index=False)

print(f"Saved: {OUT_ACTORS}, {OUT_DIRECTORS}, {OUT_ACTS_IN}, {OUT_DIRECTS}")
