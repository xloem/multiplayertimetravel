# for designing an interface of system simulation

# a simple system where some property is a function of time.

# goal 1: user has access to a state containing a number, and can produce
#         another state based on a time change from the first
#         number = constant * time

# goal 2: model user in a way that can be simulated, and let them mutate
#         the constant, spawning temporal uncertainty. the simulation can
#         be simply a uniform distribution of chance of change.

# goal 3: simulate a single timeline, letting the user move along it arbitrarily

# goal 4: simulate multiple timelines, with an interface as to whether to bind
#         actions to one or spawn a new one.  be nice to have that be a float
#         probability of binding.

class AdvancingNumberUniverse:
