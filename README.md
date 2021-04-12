# sp21-cs242-project: mpviz Week 2

## Description

This week, I implemented various algorithms to compute some static information based on users. All the information I computed is available as an API hosted in flask. I then started working on the data visualization.

## Example Execution

- get user info: python3 src/api/query.py -q '200305518?user'
- get route info: python3 src/api/query.py -q '106333612?user'
- get common ticks: python3 src/api/query.py -q '200305518&200696013?tick'
