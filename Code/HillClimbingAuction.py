import copy
import numpy as np

def hill_climb_v1(manager):
    curr_hand = copy.deepcopy(manager.played_cards)
    if not curr_hand:
        curr_hand = []
    turn = manager.turn 
    
    left_hand = copy.deepcopy(manager.left_bot_cards)
    right_hand = copy.deepcopy(manager.right_bot_cards)
    top_hand = copy.deepcopy(manager.top_bot_cards)
    main_hand = copy.deepcopy(manager.main_cards)
    
    hands = [main_hand, left_hand, top_hand, right_hand]
    
    trump_cards: list[int] = [11, 4, 3, 20, 10, 14, 0, 0]
    no_trump_cards: list[int] = [19, 4, 3, 2, 10, 0, 0, 0]
    friend_suit = None
    friend_bid = manager.auction_players_bids[(turn + 2) % 4]
    
    if not friend_bid or friend_bid[-1][0] == "Pass":
        friend_bid = 0
    else:
        friend_suit = friend_bid[-1][1]
        friend_bid = friend_bid[-1][0]
        
    curr_hand = hands[turn]
    
    costs = [[0,0], [1,0], [2,0], [3,0], [4,0]]
    for i in range(4):
        for card_obj in curr_hand:
            card = card_obj.card
            if card[1] == i:
                costs[i][1] += trump_cards[card[0]]
        if friend_suit == i:
            costs[i][1] += friend_bid / 2
    
    for card_obj in curr_hand:
        card = card_obj.card
        costs[4][1] += no_trump_cards[card[0]]
        
    if friend_suit == 4:
        costs[4][1] += friend_bid / 2
        
    costs[4][1] = costs[4][1] / 2
            
    costs = sorted(costs, key=lambda l:l[1], reverse=True)
    bid = int((costs[0][1] / 20) + 0.5) 
    suit = costs[0][0]
    

    if manager.auction_start_num * 3.5 > costs[0][1]:
        return ("Pass", 0)
    
    return (bid, suit) 

def hill_climb_v2(manager):
    curr_hand = copy.deepcopy(manager.played_cards)
    if not curr_hand:
        curr_hand = []
    turn = manager.turn 
    
    left_hand = copy.deepcopy(manager.left_bot_cards)
    right_hand = copy.deepcopy(manager.right_bot_cards)
    top_hand = copy.deepcopy(manager.top_bot_cards)
    main_hand = copy.deepcopy(manager.main_cards)
    
    hands = [main_hand, left_hand, top_hand, right_hand]
    
    trump_cards: list[int] = [11, 4, 3, 20, 10, 14, 0, 0]
    no_trump_cards: list[int] = [19, 4, 3, 2, 10, 0, 0, 0]
    friend_suit = None
    friend_bid = manager.auction_players_bids[(turn + 2) % 4]
    
    if not friend_bid or friend_bid[-1][0] == "Pass":
        friend_bid = 0
    else:
        friend_suit = friend_bid[-1][1]
        friend_bid = friend_bid[-1][0]
        
    curr_hand = hands[turn]
    
    costs = [[0,0], [1,0], [2,0], [3,0], [4,0]]
    for i in range(4):
        for card_obj in curr_hand:
            card = card_obj.card
            if card[1] == i:
                costs[i][1] += trump_cards[card[0]]
        if friend_suit == i:
            costs[i][1] += friend_bid / 1.5 #was 2
    
    for card_obj in curr_hand:
        card = card_obj.card
        costs[4][1] += no_trump_cards[card[0]]
        
    if friend_suit == 4:
        costs[4][1] += friend_bid / 1.5 #was 2
        
    costs[4][1] = costs[4][1] / 1.7 #was 2
            
    costs = sorted(costs, key=lambda l:l[1], reverse=True)
    bid = int((costs[0][1] / 20)) #Round down instead of up
    suit = costs[0][0]
    

    if manager.auction_start_num * 4.5 > costs[0][1]: #was 4
        return ("Pass", 0)
    
    return (bid, suit) 