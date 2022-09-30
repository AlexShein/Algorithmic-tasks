from math import copysign


class User:
    rank = -8
    progress = 0

    def inc_progress(self, kata_level: int) -> None:
        if kata_level > 8 or kata_level < -8 or kata_level == 0:
            raise ValueError('Invalid kata level')
        if (kata_level < self.rank - 1 - self._around_zero(kata_level, self.rank)) or (self.rank == 8):
            return

        reward = self._reward(kata_level)
        self.progress += reward
        lvl_up = self.progress // 100

        self.rank += lvl_up + self._around_zero(self.rank, self.rank + lvl_up)
        self.progress = self.progress % 100
        if self.rank == 0:
            self.rank = 1
        elif self.rank >= 8:
            self.rank = 8
            self.progress = 0

    def _reward(self, kata_level: int) -> int:
        if kata_level < self.rank:
            return 1
        elif kata_level == self.rank:
            return 3
        else:
            return 10 * ((abs(kata_level - self.rank) - self._around_zero(kata_level, self.rank)) ** 2)

    @staticmethod
    def _around_zero(val1: int, val2: int) -> int:
        return int(copysign(1, val1) != copysign(1, val2))

    def __str__(self):
        return f'User {self.rank=} {self.progress=}'


if __name__ == '__main__':
    user = User()
    assert user.rank == -8
    assert user.progress == 0
    user.inc_progress(-7)
    assert user.progress == 10
    user.inc_progress(-5)
    assert user.progress == 0
    assert user.rank == -7
