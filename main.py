from src.game import Game

game = Game()

while game.running:
    game.current_menu.display_menu()

    while game.playing:
        game.game_loop()