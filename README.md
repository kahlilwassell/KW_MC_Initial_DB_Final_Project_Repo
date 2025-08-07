# Project Overview
Contirbutors : Kahlil Wassell and Matt Chen
App: Movie Rating & Discovery
Stack: Neo4j (DB), Python

Core Features:
1. User profiles, ratings, watchlists
2. Friendships and "friend-of-friend" logic
3. Movie discovery by genres, actors, directors
4. Recommendation system using ratings and social graph

## Timeline Plan (Aug 6 - Aug 18)
### Aug 6-7 (Today-Tomorrow): Finalize Design and Data
- [ ] Clean and structure your dataset to fit the Neo4j model
- [ ] Define and finalize your graph schema in Neo4j
Nodes: User, Movie, Actor, Director, Genre, Watchlist
Relationships: RATED, HAS_WATCHLIST, INCLUDES, FRIENDS_WITH, DIRECTED, FEATURED_IN, HAS_GENRE

### Aug 8–10 (Thurs–Sat): Backend App and Data Load Scripts
Build a Python script to load users, movies, connections, etc. into Neo4j
Add logic to avoid duplicates
- [ ] Implement core functions:
- [ ] Add movie to watchlist
- [ ] Rate a movie
- [ ] View friend's or friend's friends' ratings
- [ ] Recommend based on friend network

### Aug 11–13 (Sun-Tues): GUI Interface
Design a simple interface that:
Lets user select a query, enter inputs, and view results.

### Aug 14–15 (Wed-Thurs): Query Implementation & Testing
- [ ] Implement queries using Cypher
- [ ] Create user friendly labels for the GUI
- [ ] Validate outputs and fix edge cases

### Aug 16 (Fri): Documentation & Final PDF
Write final report:
- [ ] Description, schema, data sources
- [ ] Final ER and  relational models (revised for graph if needed)
- [ ] Screenshots of app and query outputs
- [ ] Final Cypher query listing

### Aug 17 (Sat): Final Testing & Polish
- [ ] Run through demo
- [ ] Polish GUI/anything else we need to tie up

### Aug 18 (Sun): Submission & Presentation Prep
- [ ] Submit PDF report