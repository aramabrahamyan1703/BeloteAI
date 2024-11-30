import copy
import time

def Alpha_Beta_Search(game, manager):
    curr_hand = copy.deepcopy(manager.played_cards)
    if not curr_hand:
        curr_hand = []
    turn = manager.turn #The terminal node is always a min node or a max node so based on the turn we can adjust it appropriately
    
    left_hand = copy.deepcopy(manager.left_bot_cards)
    right_hand = copy.deepcopy(manager.right_bot_cards)
    top_hand = copy.deepcopy(manager.top_bot_cards)
    main_hand = copy.deepcopy(manager.main_cards)
    
    hands = [main_hand, left_hand, top_hand, right_hand]
    val = Max_Value(curr_hand, turn, hands, -1000, 1000, game, manager,  0, 0)
    return val[1]
    
def Max_Value(curr_hand: list, turn: int, hands: list[list], alpha: int, beta: int, game, manager, our_score, depth_limit):
    flag = False
    #All hands empty
    for i in hands:
        if i != []:
            flag = True
    
    #If all empty it's the terminal state, return the score
    if not flag:
        return (calculate_score(our_score, manager), 0)
    
    if depth_limit >= 11:
        return (our_score / 10, 0)

    if len(curr_hand) == 4:
        hand_and_turn = get_value(curr_hand, turn, game, 0)
        our_score += hand_and_turn[0]
        turn = hand_and_turn[1]
        curr_hand = []
        
    val = (-1000, 0)
    for index, card in enumerate(get_valid_cards(hands[turn], curr_hand, game)):
        
        curr_hand.append(card)    
        hands[turn].remove(card)
                
            
        #If curr_hand is full get the score of the current hand
            
        if turn == 0 or turn == 2:
            min_val = Min_Value(curr_hand, (turn + 1) % 4 if flag else turn, hands, alpha, beta, game, manager, our_score, depth_limit + 1)
        else:
            min_val = Max_Value(curr_hand, (turn + 1) % 4 if flag else turn, hands, alpha, beta, game, manager, our_score, depth_limit + 1)

        
        curr_hand.remove(card)
        hands[turn].append(card)
        
        if min_val[0] >= val[0]:
            val = (min_val[0], index)
        
        alpha = max(alpha, val[0])
        
        if alpha >= beta:
            return val
        
    return val
        
def Min_Value(curr_hand: list, turn: int, hands: list[list], alpha: int, beta: int, game, manager, our_score, depth_limit):
    flag = False

    for i in hands:
        if i != []:
            flag = True
            
    if not flag:
        if len(curr_hand) == 4:
            return (calculate_score(our_score, manager), 0)
        
    if depth_limit >= 11:
        return (our_score / 10, 0)
    
    if len(curr_hand) == 4:
        hand_and_turn = get_value(curr_hand, turn, game, 0)
        our_score += hand_and_turn[0]
        turn = hand_and_turn[1]
        curr_hand = []
        flag = False
        
    val = (1000, 0)
    for index, card in enumerate(get_valid_cards(hands[turn], curr_hand, game)):
        
        curr_hand.append(card)
        hands[turn].remove(card)
        
        
        if turn == 0 or turn == 2:
            max_val = Min_Value(curr_hand, (turn + 1) % 4 if flag else turn, hands, alpha, beta, game, manager, our_score, depth_limit + 1)
        else:
            max_val = Max_Value(curr_hand, (turn + 1) % 4 if flag else turn, hands, alpha, beta, game, manager, our_score, depth_limit + 1)
        
        curr_hand.remove(card)
        hands[turn].append(card)
        
        if max_val[0] <= val[0]:
            val = (max_val[0], index)
        
        beta = min(beta, val[0])
        
        if beta <= alpha:
            return val
        
    return val

def calculate_score(our_score, manager):
    their_score = 162 - our_score
    #We made the final auction
    if manager.auction_result[3] == 0:    
        if our_score < manager.auction_result[2] * 10:
            return 0
        our_score = manager.auction_result[2] + int((our_score / 10) + 0.4) 
        their_score = 16 - int((our_score / 10) + 0.4) 
        return our_score
    
    #They made the final auction
    if manager.auction_result[3] == 1:     
        if their_score < manager.auction_result[2] * 10: #CHANGE TO 10
            our_score = 16 + manager.auction_result[2]
            return our_score
        their_score = manager.auction_result[2] + int((their_score / 10) + 0.4) 
        our_score = 16 - int((their_score / 10) + 0.4) 
        return our_score

def get_value(curr_hand: list[list[int, int]], turn, game, last):
    score = 0
    cards = []
    
    for card in curr_hand:
        cards.append(card.card)
        
    for card in cards:
        score += game.get_card_value(card)
    
    turn = (turn + 1) % 4
    
    turn = (turn + game.who_takes(cards)[0]) % 4 
    score = score + 10 if last else score
    return (score, turn) if turn % 2 == 0 else (0, turn)

def get_valid_cards(cards, curr_hand, game):
        #This method uses so many if-s you might as well call it AI.
        valid_cards = []
        trump_cards_vals: list[int] = [11, 4, 3, 20, 10, 14, 0, 0]
        suit = curr_hand[0] if len(curr_hand) > 0 else None
        
        if suit == None:
            return cards
        
        if game.trump_suit == 4:
            #If you have cards of the same suit
            for card_obj in cards:
                if card_obj.card[1] == suit:
                    valid_cards.append(card_obj)         
                    
            #If not, any card         
            return valid_cards if valid_cards else cards
        
        temp = []
        for i in curr_hand:
            temp.append(i.card)
        
        who_takes = game.who_takes(temp)
    
        if suit == game.trump_suit:
            #If you have bigger trump
            max_val = 0
            for card_obj in curr_hand:
                if card_obj.card[1] == suit:
                    if max_val < trump_cards_vals[card_obj.card[0]]:
                        max_val = trump_cards_vals[card_obj.card[0]]
                    
            for card_obj in cards:
                if card_obj.card[1] == game.trump_suit and trump_cards_vals[card_obj.card[0]] > max_val:
                    valid_cards.append(card_obj)
                    
            #If not, If you have any trumps
            if not valid_cards:
                for card_obj in cards:
                    if card_obj.card[1] == suit:
                        valid_cards.append(card_obj)
            #If not, any card
            return valid_cards if valid_cards else cards
        
        #Check if there is a trump
        trump_in_deck = False
        for card_obj in curr_hand:
            if card_obj.card[1] == game.trump_suit:
                trump_in_deck = True
                break
        
        if trump_in_deck:
            #If you have cards of the same suit
            for card_obj in cards:
                if card_obj.card[1] == suit:
                    valid_cards.append(card_obj)
                     
            #If not, If you have bigger trump cards
            if not valid_cards:
                if len(curr_hand) > 1:
                    if len(curr_hand) - 2 == who_takes[0]:
                        return cards
                    
                max_val = 0
                for card_obj in curr_hand:
                    if card_obj.card[1] == suit:
                        if max_val < trump_cards_vals[card_obj.card[0]]:
                            max_val = trump_cards_vals[card_obj.card[0]] 
                
                for card_obj in cards:
                    if card_obj.card[1] == game.trump_suit and trump_cards_vals[card_obj.card[0]] > max_val:
                        valid_cards.append(card_obj)
            
            #If not, every card    
            return valid_cards if valid_cards else cards
                
        
        #If you have cards of the same suit
        for card_obj in cards:
            if card_obj.card[1] == suit:
                valid_cards.append(card_obj)         
        
        #If not, if you have trump cards       
        if not valid_cards:
            if len(curr_hand) > 1:
                if len(curr_hand) - 2 == who_takes[0]:
                    return cards
                
            for card_obj in cards:
                if card_obj.card[1] == game.trump_suit:
                    valid_cards.append(card_obj)
                    
        #If not, any card         
        return valid_cards if valid_cards else cards