# mpviz: A Mountain Project Visualization Tool
William Jiang (whjiang3) | Moderator: Miranda Liu (minerl2) <br>
See what you have in common with climbers on Mountain Project! <br>
Grading Rubric: https://docs.google.com/spreadsheets/d/1FvU92ir20-y8lPS7U3yCi-RGU1vfaOyKTCwAWLibZpU/edit?usp=sharing
## Abstract
### Project Purpose
The purpose of this project is to enhance and augment the Mountain Project user experience by allowing users to visualize their ticks and to-dos in relation to other users.
### Project Motivation
Mountain Project (https://mountainproject.com, MP from here on) is a site that houses crowd-sourced information specific to climbers. Essentially, climbers can create pages for climbing areas across the U.S. (and abroad) and within those areas, create pages for very specific climbing routes or bouldering problems. A climbing route is a general term for a specific way to scale a formation, usually determined by a sequence of moves, and a bouldering problem is a climbing route on a boulder. The value in having this information crowd-sourced is that a climber may be interested in climbing a route, but may not know where this route is, so they may look up this route on MP and find that other users have described exactly where the route they're looking for is. MP tends to beat guidebooks in several ways, one way being that it is free and another way being that the information is always extremely up to date.

There is a function on MP that allows climbers to take the routes that they climb and indicate that they have climbed them successfully-- a "tick". You can go on anyone's profile and view all of the climbs that person has ever ticked, as well as a breakdown of then they occurred, how difficult the climb was, and a general sense of where the climb was.

Built into the soul of MP is its ability to facilitate social interactions between climbers over the internet: there is a forum that connects climbers across the country and a partner finder for those in need of people to climb with. However, I think there is a dimension missing, which is that climbers should be able to very easily compare each other based on what they have climbed. Thus, my project aims to satisfy this missing component, by providing climbers with a means to compare each other, based on criterion like where they have climbed together, what grades they have climbed the same, and what they would like to climb together in the future.
## Technical Specification
- Platform: Cross-platform website (React Native)
- Programming Languages: Javascript for frontend, Python for backend
- Stylistic Conventions: Airbnb JavaScript Style Guide, PEP8
- SDK: Facebook SDK for React Native
- IDE: Atom
- Tools/Interfaces: sigma.js for network visualization, Flask to deploy site
- Target Audience: MP users

## Functional Specification
### Features
- It can take as input two MP users
- It can display the two users ticks and to-dos as a network
- It can display other information about things in common between users

### Scope of the project
- Limitations: compare only 2 users to keep visualization non-messy
- Assumptions: that users would find these visualizations useful

## Brief Timeline
- Week 1: web scraping for users and routes, database integration
- Week 2: create fixed visualizations on fixed inputs, compute key information and make accessible as API
- Week 3: make website to host visualizations, make website display non-interactive information
- Week 4: make visualizations interactive on website

## Rubrics
### Week 1: web scraping, database integration
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| User Scraping | 5 | +1: Name (string) <br> +1: Region, Age, Gender (string, int, string) <br> +1: Ticks (list of strings) <br> +1: To-do's (list of strings) <br> +1: Picture URL (string) <br> |
| Route Scraping | 5 | +1: Name (string) <br> +1: Type (string) <br> +1: Difficulty (string) <br> +1: FA (string) <br> +1: Picture URL (string) <br> |
| Database | 4 | 0: Didn't implement anything <br> 2: Writes to database w/o errors <br> 4: Read/write to database w/o errors |
| .env |  1  |  +1: Stores sensitive information as environment variable |
| Unit Testing |  10  | +1 per unit test |

### Week 2: fixed visualization, compute baseline information, API
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Visualization | 5 | +1: Render user in network <br> +1: Render ticks in network <br> +1: Render to-do's in network <br> +1: Render two users in network <br> +1: Connect user's ticks and to-do's together|
| Visualization Aesthetics | 3 | +1: Visualization uses color to indicate user node vs. route node <br> +1: Visualization uses size to indicate how popular a climb is <br> +1: Visualization renders nodes such that they are not too crowded |
| Computation on dataset | 5 | +1: Computes the number of ticks in common and what they are <br> +1: Computes the number of to-do's in common and what they are <br> +1: Computes the most popular climb in tick list exclusive to either climber <br> +1: Computes least popular climb exclusive to either climber <br> +1 Computes hardest tick for either climber in any discipline |
| Computation API | 2 | +2: Makes computed information available as API |
| Manual Test Plan |  5  | +1 per page of manual test plan for visualization |
| Unit testing |  5  | +.5 for each unit test on computations and API |

### Week 3: website, display key information
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| Render Key Content | 4.5 | +1: Website takes two users as input <br> +1: Reports errors on finding users <br> +0.5 for each of the 5 key information computed in week 2 |
| Website Aesthetics | 5 | +1: Website is contained in a single view <br> +1: Website allows navigation to start input view <br> +1: Website incorporates aesthetic color and fonts <br> +5: Website renders well on variety of platforms <br> +1: Website has attractive loading screen |
| Website Sketch | 3.5 | +3.5: Detailed sketch of the website view |
| ESlint | 2 | +2 presence of eslint |
| Manual Test Plan | 10 | +1 per page of manual test plan |

### Week 4: make visualization interactive on website
| Category  | Total Score Allocated | Detailed Rubrics                                                            |
|-----------|:---------:|-------------------------------------------------------------------------------|
| User Node View | 4 | +1: User view contains name <br> +1: User view displays age <br> +1: User view displays profile picture <br> +1: User view displays creation date |
| Route Node View | 4 | +1: Route view contains name <br> +1: Route view displays type <br> +1: Route view displays FA <br> +1: Route view displays first picture |
| Visualization responds to mouse controls | 5 | +1: dragging around visualization moves to different part of network <br> +1: scrolling in and out zooms in and out of network <br> +1: Clicking on user node displays user node view <br> +1: Clicking on route node displays route node view <br> +1: Clicking on visualization removes any view overlay |
| Website Integration | 2 | +1: Visualization renders on separate page <br> +1: Visualization page has buttons for navigation back to the main page |
| Manual Test Plan | 10 | +1 per page of manual test plan|
