import random, time

# Time 11
# #########################################
# # World 0 (modeled blind to any others) #
#  data = 275
#  agents = ['B']
# ~~~~ Bing! A appears ~~~~
# #########################################

class BigThing:
    def __init__(self, **attrs):
        self._attrs = attrs
        for name, val in attrs.items():
            setattr(self, name, val)
    def __str__(self):
        return str(next(iter(self._attrs.values())))

class P:
    def stability(self):
        return max([prob for val, prob in self])
    def sample(self):
        return random.choices([val for val, prob in self], [prob for val, prob in self])[0]
class PConst(P):
    def __init__(self, val):
        self.value = val
    def __iter__(self):
        yield [self.value, 1.0]
class PSimple(P):
    def __init__(self, probs_by_val):
        self.choices = list(probs_by_val.keys())
        self.weights = list(probs_by_val.values())
        self.size = len(probs_by_val)
    def __iter__(self):
        for x in range(self.size):
            yield [self.choices[x], self.weights[x]] # simplify
class PCombined(PSimple):
    # for flattening multiple possible resulting events
    def __init__(self, probs_by_val_by_prob):
        probs_by_val = {}
        for prob, dist in probs_by_val_by_prob.items():
            for val, subprob in dist.items():
                probs_by_val[val] = probs_by_val.get(val, 0) + subprob * prob
        super().__init__(probs_by_val)

class FakeTimeline: # change to TeleportationNegotiation or such
    def __init__(self, known_point):
        self.anchor = known_point
    # def expand(self,

# All probability content above. Have not turned
# universe into tree of possibilities. Just emotionally
# challenging.

class Region(BigThing):
    def __init__(self, universe, real=False, **attrs):
        super().__init__(**attrs)
        self.universe = universe
        self.universe.regions.append(self)
        self.real = real
        self.agents = set()
    def tick(self, time):
        pass
    @property
    def other_regions(self):
        return [region for region in self.universe.regions if region is not self]

class Miniverse:
    def __init__(self):
        self.regions = []
        self.time = 0
    def tick(self):
        self.time += 1
        for region in self.regions:
            region.tick(self.time)
        # tick all agents after all regions for fair&acc order
        for agent in [agent
                    for region in self.regions
                      for agent in region.agents]:
            agent.tick(agent.region, self.time)

class Agent(BigThing):
    def __init__(self, region, **attrs):
        super().__init__(**attrs)
        self.region = region
        self.region.agents.add(self)
    def teleport(self, region):
        if self.region.real:
            print(f'~~~~ Pop! {self} disappears ~~~~')
        elif region.real:
            print(f'~~~~ Bing! {self} appears ~~~~')
        region.agents.add(self)
        self.region.agents.discard(self)
        self.region = region
    def clone(self, region):
        return Agent(region, **self._attrs)

def create_model(idx, total):
    class SimpleRegion(Region):
        def __init__(self, universe, seed=None, **attrs):
            super().__init__(universe, **attrs)
            self.rand = random.Random(x=seed)
            self.tick(0)
        def tick(self, time):
            self.data = self.rand.randint(0, 256)
            super().tick(time)
        def clone(self):
            region = SimpleRegion(None, **self._attrs)
            region.agents = set([agent.clone for agent in self.agents])
            region.rand.setstate(self.rand.getstate())
            return region
    miniverse = Miniverse()
    for region_idx in range(total):
        SimpleRegion(miniverse, seed=region_idx, real=idx==region_idx).idx = region_idx

    A = Agent(miniverse.regions[0], name='A')
    A.tick = lambda region, time: A.teleport(region.other_regions[0]) if region.data % 4 == 2 else None

    B = Agent(miniverse.regions[1], name='B')
    B.tick = lambda region, time: B.teleport(region.other_regions[0]) if region.data % 8 == 4 else None

    return miniverse.regions[idx]

def main():
    worlds = [create_model(idx, 2) for idx in range(2)]

    # needs uncertainty of data or tick, make trees

    while True:
        print('Time', worlds[0].universe.time)
        for world in worlds:
            print('#######'+ '###'     +'###############################')
            print('# World', world.idx, '(modeled blind to any others) #')
            print(' data =', world.data)
            print(' agents =', [agent.name for agent in world.agents])
            world.universe.tick() # Bing! A appears
            assert world.universe.time == worlds[0].universe.time
            print('#######'+ '###'     +'###############################')
            print()
        print()
        time.sleep(2)

if __name__ == '__main__':
    main()
