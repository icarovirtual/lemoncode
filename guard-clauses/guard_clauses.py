# -*- coding: utf-8 -*-


def func_not_guarded(self, param):
    if param == 'something':
        self.counter += 1
        if self.counter > 10:
            self.reached_ten()
        else:
            if self.counter < 5:
                self.has_not_reached_5()
            else:
                self.has_not_reached_5()
    else:
        self.counter -= 1


def func_guarded(self, param):
    if param != 'something':
        self.counter -= 1
        # You can call return even if the function doesn't return anything
        return
    # Important path in a low indentation level
    self.counter += 1
    if self.counter > 10:
        self.reached_ten()
        return
    # By returning early, you don't need `else` statements
    if self.counter < 5:
        self.has_not_reached_5()
        return
    self.has_not_reached_5()
