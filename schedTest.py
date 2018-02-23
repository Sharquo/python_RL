from scheduling_system import TimeSchedule

class Thing(object):
    """
        Just something to test.
        Assumes that the maximum speed of a thing is 10.
    """

    BASE_TIME = 15.0

    def __init__(self, id, speed):
        self.id = id
        self.speed = speed

    def __str__(self):
        return self.id

    def actionDelay(self):
        return Thing.BASE_TIME / self.speed

TURN_ROUNDS = 3

if __name__ == '__main__':
    things = [Thing('a', 1), Thing('b', 3), Thing('c', 5)]
    q = TimeSchedule()

    turns = 0
    turnsTaken = {}
    for t in things:
        q.scheduleEvent(t, t.actionDelay())
        turns += t.speed
        turnsTaken[t] = 0

    turns *= TURN_ROUNDS

    while turns > 0:
        thing = q.nextEvent()

        turnsTaken[thing] += 1
        print (thing)
        turns -= 1

        q.scheduleEvent(thing, thing.actionDelay())