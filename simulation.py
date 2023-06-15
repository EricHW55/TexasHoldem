from Texasholdem import env
import random
from copy import deepcopy
from tqdm import trange
from typing import Tuple


class Simulation:
    def __init__(self):
        self.env = env()


    def __call__(self, num:int, community_card:list, my_hand:list, opponent_hand:list, opponent_action_num:int, pot_size:int=0, loss:int=0) -> int: # 시뮬레이션 결과 반환
        action_results = [0,0,-1*num] # -1*num : 참가비 1$
        for n,action in enumerate([0,1]): # action
            for i in range(num):
                self.community_card = deepcopy(community_card)
                self.my_hand = deepcopy(my_hand); self.opponent_hand = deepcopy(opponent_hand)
                _loss, pot_size = self.simulation(opponent_action=opponent_action_num, agent_action=action, pot_size=pot_size, loss=loss) # <<<
                action_results[n] += _loss
        print(action_results)
        return action_results.index(max(action_results))


    def simulation(self, opponent_action:int, agent_action:int, pot_size:int, loss:int) -> int: # 시뮬레이션
        # 상대방 action에서 fold 제외, 남은 공동카드 2장 랜덤으로 action이 목표, 손실률만 계산
        shapes = ['♠', '♡', '♢', '♣']
        left_deck = [(s,i) for s in shapes for i in range(2, 15)]
        for i in self.community_card + self.my_hand + self.opponent_hand: # + self.opponent_hand 부분
            left_deck.remove(i) # 남은 카드들

        # if self.community_card == 3: # 첫번째 베팅
        def betting_phase_simulation(action_num:int, loss:int, pot_size:int, _random:bool, agent_action:int) -> tuple:
            action_list = [0, 1] # 0: check, 1 : raise
            opponent_betting = 2 if action_list[action_num] else 0
            my_betting = 0

            action = random.choice(action_list) if _random else agent_action

            if not action: # check (check - check or raise - check)
                loss -= (opponent_betting - my_betting)
                pot_size += (opponent_betting - my_betting)

            elif action:  # raise
                # betting *= 2
                my_betting = opponent_betting*2 if opponent_betting else 2 # 2배 or 2
                loss -= my_betting
                pot_size += my_betting

                if not my_betting == 4: # check - raise
                    opponent_action = random.choice(action_list)
                    if not opponent_action: # check - raise - call
                        # call
                        pot_size += (my_betting - opponent_betting) # 상대방 check 기준
                    elif opponent_action : # check - raise - raise - call
                        # raise
                        opponent_betting = my_betting*2
                        pot_size += opponent_betting

                        # call
                        loss -= (opponent_betting - my_betting)
                        pot_size += (opponent_betting - my_betting)
                else: # raise - raise - call
                    # raise
                    my_betting = opponent_betting*2
                    loss -= my_betting
                    pot_size += my_betting

                    # call
                    pot_size += (my_betting - opponent_betting)
            
            my_betting, opponent_betting = 0, 0
            return loss, pot_size

        loss, pot_size = 0, 0
        _random = False
        if len(self.community_card) == 3:
            loss, pot_size = betting_phase_simulation(action_num=opponent_action, loss=loss, pot_size=pot_size, _random=False, agent_action=agent_action)
            new_community_card = random.sample(left_deck, 2)
            self.community_card += new_community_card
            _random = True
            agent_action = random.choice([0, 1])
        
        if len(self.community_card) == 5:
            loss, pot_size = betting_phase_simulation(action_num=opponent_action, loss=loss, pot_size=pot_size, _random=_random, agent_action=agent_action)
        

        results = env.compare_hand(community_card=self.community_card, opponent_hand=self.opponent_hand, my_hand=self.my_hand)
        
        if results == True : # 승
            loss += pot_size
        elif results == False : # 패
            None
        elif results == None : # 무
            loss += (pot_size/2)

        return loss, pot_size

        # 
        
        
        # if self.community_card == 5: # 마지막 베팅
        #     opponent_action = random.sample(action_list)

        #     if not opponent_action : # check
        #         # pot_size += betting
        #         ...

        #     elif opponent_action : # raise
        #         pot_size += betting
            

        #     action = random.sample(action_list)

        #     if not action: #check


            

        # if action_list[action_num]:
        #     loss -= betting_size
        #     pot_size += betting_size
        #     betting_size *= 2
            
        #     opponent_action = random.sample(action_list)
        #     if opponent_action: # raise
        #         pot_size += betting_size

        
        

        



if __name__ == '__main__':
    env = env()
    sim = Simulation()

    community_card = env.draw(input_deck=[], num=3)
    print('Community Card :', community_card)
    
    hand = env.draw(input_deck=[], num=2)
    print('Opponent Hand :', hand)

    hand2 = env.draw(input_deck=[], num=2)
    print('My Hand :', hand2)

    action_list = ['Check', 'Raise', 'Fold']
    # my_action = 0 # 0 : check, 1 : raise, 2 : folds
    my_action = int(input('Action(0:check, 1:raise, 2:fold) : '))
    action_num = sim(num=600, community_card=community_card, my_hand=hand, opponent_hand=hand2, opponent_action_num=my_action, pot_size=0, loss=0)
    print(action_list[action_num])

    community_card = env.draw(input_deck=community_card, num=2)

    print('Community Card :', community_card)
    print('Opponent Hand :', hand)
    print('My Hand :', hand2)

    my_action = int(input('Action(0:check, 1:raise, 2:fold) : '))
    action_num = sim(num=600, community_card=community_card, my_hand=hand, opponent_hand=hand2, opponent_action_num=my_action, pot_size=0, loss=0)
    print(action_list[action_num])

    
    results = env.compare_hand(community_card=community_card, opponent_hand=hand, my_hand=hand2)
    if results == True:
        print('승')
    elif results == None:
        print('무')
    else :
        print('패')