from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError

class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float=60*15,*args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type,name,time_limit,*args)


    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        # Prendre les actions possibles de l'état initial     
        possible_actions = current_state.get_possible_actions()
        # Initialiser la meilleure action à None ainsi que le meilleur score à -inf (valeur la plus basse pour le maximiseur)
        best_action = None
        best_score = float('-inf')
        # Itérer sur toutes les actions possibles pour descendre dans l'arbre d'états
        for action in possible_actions:
            # Passer au prochain état après avoir appliquer l'action
            next_state = action.get_next_game_state()
            # Utiliser l'algorithme de minimax pour récursivement traverser les états de l'arbre
            # Depth est la profondeur de la recherche avant de remonter un score
            score = self.minimax(next_state, depth=1, maximizing_player=True)

            # Si un meilleur score est trouvé, mettre à jour le meilleur score avec l'action associée
            if score > best_score:
                best_score = score
                best_action = action
        print(best_score)
        print(best_action)
        # Retourner la meilleure action à faire
        return best_action
    
    # Algorithme minimax
    def minimax(self, state: GameState, depth: int, maximizing_player: bool) -> int:
        #Si nous avons fini de découvrir ou il n'y a plus d'états à découvrir (fin de partie)
        if depth == 0 or state.is_done():
            # On évalue le score de l'état avec la fonction heuristique
            return self.value_state(state)
        # Si le tour est au maximiseur, on maximise le score
        if maximizing_player:
            max_score = float('-inf')
            for action in state.get_possible_actions():
                next_state = action.get_next_game_state()
                score = self.minimax(next_state, depth - 1, False)
                max_score = max(max_score, score)
            return max_score
        else:
            # Si le tour est au minimiseur, on minimise le score
            min_score = float('inf')
            for action in state.get_possible_actions():
                next_state = action.get_next_game_state()
                score = self.minimax(next_state, depth - 1, True)
                min_score = min(min_score, score)
            return min_score

    # Fonction heuristique pour l'évaluation d'un état
    def value_state(self, state: GameState) -> int:
        #number of pieces
        #center control
        #mobility

        # Weight parameters for the heuristic components
        piece_count_weight = 1.0
        # center_control_weight = 1.5
        # mobility_weight = 0.5

        # Evaluate piece count
        # print(state.get_rep().get_env())
        piece_count = len(state.get_rep().get_env())  # Adjust if necessary based on your GameState implementation
        # print(piece_count)
        # print(self.get_id())
        # print(self.get_name())
        # print(self.get_piece_type())
        # # Evaluate center control
        # center_control = sum(1 for piece in state.get_rep().get_pieces() if state.is_in_center(piece.get_position()))

        # # Evaluate mobility
        # mobility = sum(len(state.get_valid_moves(piece)) for piece in state.get_rep().get_pieces())

        # # Combine the components with their respective weights
        # score = (
        #     piece_count_weight * piece_count +
        #     center_control_weight * center_control +
        #     mobility_weight * mobility
        # )
        score = piece_count_weight*piece_count

        return score
    
#     # Example is_in_center function (adjust based on the actual structure of your board)

#  def is_in_center(piece_position):
#     center_row_start, center_row_end = 4, 11
#     center_col_start, center_col_end = 4, 11
#     row, col = piece_position  # Adjust based on your GameState implementation

#     return center_row_start <= row <= center_row_end and center_col_start <= col <= center_col_end