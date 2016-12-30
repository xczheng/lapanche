from enum import Enum
from collections import deque
import random

class Color(Enum):
    HEART = "红桃"
    DIAMOND = "方块"
    SPADE = "黑桃"
    CLUB = "梅花"

class Card(object):
    special_card_map = {
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
            15: '小王',
            16: '大王',
    }
    switched_card_map = {y:x for x,y in special_card_map.items()}
    def __init__(self, number, color=None):
        if color is None:
            if type(number) == int:
                if number not in (15, 16):
                    raise "color can't be empty"
                else:
                    self.number = number
                    return
            elif type(number) == str:
                if number not in ('小王', '大王'):
                    raise "color can't be empty"
                else:
                    self.number = Card.switched_card_map[number]
                    return
                
        if type(color) != Color:
            raise "color must be a Color!"
        self.color = color
        if type(number) == int:
            self.number = number
            return
        try:
            self.number = int(self.number)
        except ValueError:
            self.number = Card.switched_card_map[number]

    def __str__(self):
        if 2 <= self.number <= 10:
            return str(self.color.value) + ' ' + str(self.number)
        if 11 <= self.number <= 14:
            return str(self.color.value) + ' ' +  Card.special_card_map[self.number]
        if self.number in (15, 16):
            return Card.special_card_map[self.number]

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other_card):
        return self.number > other_card

    def __lt__(self, other_card):
        return self.number < other_card

    def __eq__(self, other_card):
        if self.number in (16, 15) and other_card.number in (16, 15):
            return True
        return self.number == other_card.number

def main():
    one_set_card = []
    for color in list(Color):
        for i in range(2, 15):
            card = Card(i, color)
            one_set_card.append(card)
    one_set_card.append(Card('大王'))
    one_set_card.append(Card('小王'))
    random.shuffle(one_set_card)
    for card in one_set_card:
        print(card)
    total_number = len(one_set_card)
    print("total number is {}".format(total_number))
    people_list = []
    people = ["图图", "画画", "爸爸"]
    for index, person in enumerate(people):
        start = (total_number * index) // len(people)
        end = (total_number * (index + 1)) // len(people)
        people_list.append((person, deque(one_set_card[start:end])))

    running_list = []
    timing = 0
    while True:
        print("running list is {}".format(running_list))
        for person in people_list:
            print("{}'s dequeue is {}".format(person[0], person[1]))

        out = 0
        for person in people_list:
            name, q = person
            if len(q) == 0:
                out += 1
                continue
            timing += 5
            while True:
                poped_card = q.popleft()
                try:
                    found_index = running_list.index(poped_card)
                    q.extend(running_list[found_index:])
                    q.append(poped_card)
                    running_list = running_list[:found_index]
                except ValueError:
                    running_list.append(poped_card)
                    break
        if out == 2:
            print("=" * 50)
            print("game over")
            for person in people_list:
                if len(person[1]) != 0:
                    print("{} won!".format(person[0]))
                else:    
                    print("{} lost".format(person[0]))
            break

    return timing

if __name__ == "__main__":
    total_time = 0
    test_times = 1
    for i in range(test_times):
        total_time += main()
    print("average time: {}".format(total_time/test_times))



