# Foreword

There are several ways to resolve original task in the challenge. And different criterias of success

1. Fast to deliver. Since we don't have load estimations etc
2. Be a step inside the strategy of development. Then data and controller layer should be considered to be compatible with next steps of development
3. Write "the most" runtime efficient code

For the first strategy it is absolutely enough to use `requests` for REST APIs. It even can be quick'n'dirty, because in reference data only dozens of repos are listed. So there is no special load expected.

For the second strategy such packages as `PyGithub` and `pybitbucket` should be considered to use. Especially, if we will need in future use authentication and some manipulation. What we have in this case? Additional layers of abstraction that should be also wrapped with some more common layer for future ease of use.

Third strategy is based on first two but with measurable improvements and usage of async queues and other techniques to optimize overall efficiency. That is good way to go once stategy 1 or 2 is already implemented. My personal believe is that optimisation should start once PoC/MVP is working.

# What is done in the demo?

There can't be done RESTful API. We can't neither update nor create resources (repos/teams or organisations in Gihub slang). So it is more HTTP API with the only GET. I have chosen 1 approach. To make it workable. By the way, if API is RESTful it it quite strange to talk about verbs besides typical CRUD pattern over existing resourses. 

We can only GET info described in original doc: 

```
Provide a RESTful way for a client to provide the Github organization and Bitbucket team
names to merge for the profile. The profile should include the following information (when available):

* Total number of public repos (seperate by original repos vs forked repos)
* Total watcher/follower count
* A list/count of languages used across all public repos
* A list/count of repo topics
```

# What to improve

Moving from 1 to 3 strategy should also include `asyncio` usage for parallel data acquisition. But my recommendation is also move to Python 3.7 (considering improvements on async run etc)