# Foreword

There are several ways to resolve original task in the challenge. And different criterias of success

1. Fast to deliver. Since we don't have load estimations etc
2. Be a step inside the strategy of development. Then data and controller layer should be considered to be compatible with next steps
3. Write "the most" runtime efficient code

For the first strategy it is absolutely enough to use `requests` for REST APIs. It even can be quick'n'dirty, because in reference data only dozens of repos are listed. So there is no special load expected.

For the second strategy such packages as `PyGithub` and `pybitbucket` should be considered to use. Especially, if we will need in future use authentication and some manipulation. What we have in this case? Additional layers of abstraction that should be also wrapped with some more common layer for future ease of use.

Third strategy is based on first two but with measurable improvements and usage of async queues and other techniques to optimize overall efficiency. That is good way to go once stategy 1 or 2 is already implemented. My personal believe is that optimisation should start once PoC/MVP is working.

# What is done in the demo?

