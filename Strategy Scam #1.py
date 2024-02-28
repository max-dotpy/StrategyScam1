#!/usr/bin/env python
# coding: utf-8

# In[1]:


from random import shuffle


# In[2]:


def determine_value_hand(cards):
    S = sum(cards)
    for _ in range(cards.count(1)):
        if S + 10 <= 21:
            S += 10
    return S


def check_split(dealer, player):
    if player[0] in [2, 3]:
        if dealer in range(2, 8):
            return True
        return False
    elif player[0] == 4:
        if dealer in [5, 6]:
            return True
        return False
    elif player[0] in [5, 10]:
        return False
    elif player[0] == 6:
        if dealer in range(2, 7):
            return True
        return False
    elif player[0] == 7:
        if dealer in range(2, 8):
            return True
        return False
    elif player[0] in [8, 1]:
        return True
    else:
        if dealer in [7, 10, 1]:
            return False
        return True


def thereis_ace(dealer, player):
    other = player[0] if player[1] == 1 else player[1]
    if other in [2, 3]:
        if dealer in [5, 6]:
            return "double"
        return "hit"
    elif other in [4, 5]:
        if dealer in [4, 5, 6]:
            return "double"
        return "hit"
    elif other == 6:
        if dealer in [3, 4, 5, 6]:
            return "double"
        return "hit"
    elif other == 7:
        if dealer in [3, 4, 5, 6]:
            return "double"
        elif dealer in [2, 7, 8]:
            return "stand"
        else:
            return "hit"
    else:
        return "stand"


def thereis_nothing(dealer, player):
    S = determine_value_hand(player)
    if S <= 8:
        return "hit"
    elif S >= 17:
        return "stand"
    elif S == 9:
        if dealer in [3, 4, 5, 6]:
            return "double"
        return "hit"
    elif S == 10:
        if dealer in [10, 1]:
            return "hit"
        return "double"
    elif S == 11:
        if dealer in [1]:
            return "hit"
        return "double"
    elif S == 12:
        if dealer in [4, 5, 6]:
            return "stand"
        return "hit"
    else:
        if dealer in [2, 3, 4, 5, 6]:
            return "stand"
        return "hit"


class Shoe:
    def __init__(self, N=8, enough_money_to_double_or_split=True):
        self.cards = [x for x in range(1, 10)] * 4 * N + [10, 10, 10, 10] * 4 * N
        self.shuffle_deck()
        self.dealer = []
        self.player = []
        self.action = None
        self.first_action = None
        self.N = N
        self.enough = enough_money_to_double_or_split

    def shuffle_deck(self):
        shuffle(self.cards)

    def draw(self, toprint=False):
        card = self.cards.pop(0)
        if toprint:
            print(card)
        return card

    def play(self):
        self.player.append(self.draw())
        self.dealer.append(self.draw())
        self.player.append(self.draw())

        if self.player[0] == self.player[1] and self.enough:
            if check_split(self.dealer[0], self.player):
                self.first_action = "split"
                ris = 0
                for _ in range(2):
                    ris += self.play_splitted()
                return ris
            else:
                self.action = thereis_nothing(self.dealer[0], self.player)
                self.first_action = self.action + ""

                return self.act()
        else:
            if 1 in self.player:
                if 10 in self.player:
                    self.first_action = "stand"
                    if self.dealer[0] in [1, 10]:
                        self.dealer.append(self.draw())
                        if determine_value_hand(self.dealer) == 21:
                            return 0
                        return 1.5
                    self.dealer.append(self.draw())
                    return 1.5
                self.action = thereis_ace(self.dealer[0], self.player)
            else:
                self.action = thereis_nothing(self.dealer[0], self.player)
            
            self.first_action = self.action + ""

            return self.act()

    def play_splitted(self):
        del self.player[1]
        self.player.append(self.draw())
        if 1 in self.player:
            self.action = "hit"
        else:
            self.action = thereis_nothing(self.dealer[0], self.player)

        if self.action == "double":
            self.action = "hit"

        return self.act(True)

    def act(self, splitted=False):
        ris = 1
        if not self.enough:
            if self.action == "double":
                self.action = "hit"

        if self.action == "double":
            self.player.append(self.draw())
            ris *= 2

        while self.action == "hit":
            self.player.append(self.draw())
            if splitted and self.player[0]==1:
                self.action = "stand"
            else:
                self.action = thereis_nothing(self.dealer[0], self.player)
            if self.action == "double":
                self.action = "hit"

        P = determine_value_hand(self.player)
        if P > 21:
            self.dealer.append(self.draw())
            return -1 * ris

        while determine_value_hand(self.dealer) < 17:
            self.dealer.append(self.draw())

        D = determine_value_hand(self.dealer)

        if D == 21:
            if P == 21:
                if len(self.player) == 2:
                    if len(self.dealer) == 2:
                        return 0
                    return ris
                else:
                    if len(self.dealer) == 2:
                        return -1 * ris
                    else:
                        return 0
            else:
                return -1 * ris
        else:
            if P == 21:
                if len(self.player) == 2 and not splitted:
                    return ris * 1.5
            if D > 21:
                return ris
            else:
                if P == D:
                    return 0
                elif P > D:
                    return ris
                else:
                    return -1 * ris
                
    def print_play(self):
        ris = self.play()
        print("Player has: ", self.player, f" ({determine_value_hand(self.player)})", "\n", 
              "Player's decision: ", self.first_action, "\n",
              "Dealer has: ", self.dealer, f" ({determine_value_hand(self.dealer)})", "\n",
              "Result: ", ris, sep="")
        return ris

    def reset(self):
        self.dealer = []
        self.player = []
        self.action = None
        self.cards = [x for x in range(1, 10)] * 4 * self.N + [10, 10, 10, 10] * 4 * self.N
        self.shuffle_deck()


# In[14]:


deck = Shoe()


# In[31]:


deck.print_play()
deck.reset()


# ----------------------------------------------------------
# # WE NOW HAVE A BLACKJACK SIMULATOR
# ----------------------------------------------------------

# In[20]:


def strat(cap, bet=5, goal=310, _print=False):
    shoe = Shoe()

    while 0 < cap < goal and cap - bet >= 0:
        cap -= bet
        if cap - bet >= 0:
            shoe.enough = True
        else:
            shoe.enough = False
        if _print:
            ris = shoe.print_play()
        else:
            ris = shoe.play()
            
        if ris == -1:
            bet *= 2
        elif ris == 0:
            cap += bet
        elif ris == 1:
            cap += 2 * bet
            bet = 5
        elif ris == -2:
            cap -= bet
            bet *= 2
        else:
            cap -= bet
            cap += 4 * bet
            bet = 5

        shoe.reset()

    return cap


# In[36]:


print(strat(155, _print=True) - 155)


# In[37]:


win = 0
lose = 0

N = 1000
CAP = 155
GOAL = 155

for _ in range(N):
    s = strat(CAP+0, goal=CAP+GOAL)
    if s >= CAP+GOAL:
        win += 1
    elif s < CAP:
        lose += 1

print(f"Probability of winning: {win / N}%")
print(f"Probability of losing: {lose / N}%")


# ## THIS MEANS YOU HAVE ~38% OF WINNING 155
# ## DO YOU KNOW YOUR PROBABILITY OF WINNING THAT AMOUNT ON A ROULETTE?
# ## THE PROBABILITY OF WINNING RED (OR BLACK) IS 18/37 = 48.65%
# ## WHICH IS ~10% MORE FOR WINNING THE SAME AMOUNT OF MONEY.
# ## THIS STRATEGY IS A SCAM! DON'T WASTE YOUR MONEY!

# In[38]:


win = 0
lose = 0

N = 1000
CAP = 1275
GOAL = 500

for _ in range(N):
    s = strat(CAP+0, goal=CAP+GOAL)
    if s >= CAP+GOAL:
        win += 1
    elif s < CAP:
        lose += 1

print(f"Probability of winning: {win / N}%")
print(f"Probability of losing: {lose / N}%")


# In[39]:


0.38 * 155 - 0.62 * 155


# In[40]:


0.649 * 500 - 0.351 * 1275


# In[41]:


-123.02499999999998 * 1000 * (-1)


# In[15]:


win = 0
lose = 0
draw = 0

for j in range(100000):
    if j % 10000 == 0:
        print(j)
    ris = deck.play()
    if ris > 0:
        win += 1
    elif ris < 0:
        lose += 1
    else:
        draw += 1
    deck.reset()

print(win / 100000, lose / 100000, draw / 100000)

