# -*- coding: utf-8 -*-


def is_platypus_bad(self):
    if self.is_mammal():
        if self.has_fur():
            if self.has_beak():
                if self.has_tail():
                    if self.can_swim():
                        # It's a platypus!
                        return True
    # Not a platypus
    return False


def is_platypus_good(self):
    # Not a platypus for everything below
    if not self.is_mammal():
        return False
    if self.has_fur():
        return False
    if self.has_beak():
        return False
    if self.has_tail():
        return False
    if self.can_swim():
        return False
    # Finally, it's a platypus!
    return True
