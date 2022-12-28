from typing import Final, Literal

import math
import discord

# define what an empty space on the board will be
FREE_SPACE: Final[str] = " "


class TicTacToeGame:
    """
    The tic tac toe game class
    The handles the game logic and what happens during the game
    """

    def __init__(self):
        self.reset_board()

    def reset_board(self):
        self.board = [[FREE_SPACE for _ in range(3)] for _ in range(3)]

    def space_free(self, pos: int) -> bool:
        """
        This function checks to see if a position on the board is free

        Parameters:
            pos (int): The position to check for. Must be 1 - 9 or it will return False.
                The first row is 0-3 second row 4-6 and third row is 7-9

        Returns:
            bool: True if the place is free if not it will return False
                It will also return False if the position is not between (& inclduing) 1-9
        """
        if 0 < pos <= 3:
            position = self.board[0][pos - 1]
        elif 3 < pos <= 6:
            position = self.board[1][pos - 4]
        elif 6 < pos <= 9:
            position = self.board[2][pos - 7]
        else:
            return False

        if position == FREE_SPACE:
            return True

        return False

    def check_draw(self) -> bool:
        """
        This checks to see if the game is over by a draw

        Returns:
            bool: if draw it returns True else False
        """
        return all(FREE_SPACE not in row for row in self.board)

    def check_win(self) -> bool:
        """
        This function is used to check for a win

        Returns:
            bool: If its a win True if not False
        """
        # Horizontal Wins
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[0] != FREE_SPACE:
                return True

        # Vertical Wins
        for i in range(3):
            if (
                self.board[0][i] == self.board[1][i]
                and self.board[1][i] == self.board[2][i]
                and self.board[0][i] != FREE_SPACE
            ):
                return True

        # Check for diagonal wins
        if (
            self.board[0][0] == self.board[1][1]
            and self.board[1][1] == self.board[2][2]
            and self.board[0][0] != FREE_SPACE
        ):
            return True
        elif (
            self.board[0][2] == self.board[1][1]
            and self.board[1][1] == self.board[2][0]
            and self.board[0][2] != FREE_SPACE
        ):
            return True

        return False

    def update_postion(self, letter: Literal["X", "O"], pos: int) -> list[str]:
        """
        This function is used to update a players position on the board

        Parameter:
            letter (Literal[str]): The letter of the player usualy X or O.
            pos (int): The position to move to

        Returns:
            list[str]: There are 4 different types of list that will be returned
                (For the sake of consistency i chose to use a list instead of a string as on of the values needs a list)
                1. ["invalid"]: this means the position is invalid
                2. ["draw"]: This means the game has ended in a draw
                3. ["win", letter: str]: This means that a player has won so it will return the player who won as well
                    eg if X wins it will return ["win", "X"]
                4. ["continue"]: This means that the move was played successfuly
                    and nothing else happened so the game can continue
        """
        if not self.space_free(pos):
            return ["invalid"]

        if 0 < pos <= 3:
            self.board[0][pos - 1] = letter
        elif 3 < pos <= 6:
            self.board[1][pos - 4] = letter
        elif 6 < pos <= 9:
            self.board[2][pos - 7] = letter

        if self.check_draw():
            return ["draw"]

        if self.check_win():
            return ["win", letter]

        return ["continue"]


class TicTacToeAI(TicTacToeGame):
    """
    Tic tac toe but with the minimax algorithm to always win or be a draw
    The ai is just to smart cause why bot is massive brain
    """

    def check_mark_win(self, mark):
        # Horizontal Wins
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[0] == mark:
                return True

        # Vertical Wins
        for i in range(3):
            if (
                self.board[0][i] == self.board[1][i]
                and self.board[1][i] == self.board[2][i]
                and self.board[0][i] == mark
            ):
                return True

        # Check for diagonal wins
        if (
            self.board[0][0] == self.board[1][1]
            and self.board[1][1] == self.board[2][2]
            and self.board[0][0] == mark
        ):
            return True

        elif (
            self.board[0][2] == self.board[1][1]
            and self.board[1][1] == self.board[2][0]
            and self.board[0][2] == mark
        ):
            return True

        return False

    def bot_move(self, letter):
        best_score, best_move = -100, None

        for row_id, row in enumerate(self.board):
            for index, key in enumerate(row):
                if key == FREE_SPACE:
                    self.board[row_id][index] = letter
                    score = self.minimax(letter, self.board, 0, False)
                    self.board[row_id][index] = FREE_SPACE
                    if score > best_score:
                        best_score = score

                        index += 1
                        if row_id == 0:
                            best_move = index
                        elif row_id == 1:
                            best_move = index + 3
                        elif row_id == 2:
                            best_move = index + 6

        return self.update_postion(letter, best_move)

    def minimax(self, bot, board, depth, isMaximizing):
        player = "X" if bot == "O" else "O"
        if self.check_mark_win(bot):
            return 100

        elif self.check_mark_win(player):
            return -100

        elif self.check_draw():
            return 0

        if isMaximizing:
            best_score = -100

            for row_id, row in enumerate(board):
                for index, key in enumerate(row):
                    if key == FREE_SPACE:
                        board[row_id][index] = bot
                        score = self.minimax(bot, board, 0, False)
                        board[row_id][index] = FREE_SPACE
                        if score > best_score:
                            best_score = score

            return best_score

        else:
            best_score = 100

            for row_id, row in enumerate(board):
                for index, key in enumerate(row):
                    if key == FREE_SPACE:
                        board[row_id][index] = player
                        score = self.minimax(bot, board, 0, True)
                        board[row_id][index] = FREE_SPACE
                        if score < best_score:
                            best_score = score

            return best_score


class TicTacToe2PlayerButton(discord.ui.Button):
    """
    Class for a single button (out of 9) on the member vs member mode for tic tac toe
    This will be used by the TicTacToe2PlayerView
    """

    def __init__(self, pos):
        self.pos = pos
        row = math.ceil(pos / 3)
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=row)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user != self.view.current_player:
            return await interaction.followup.send(
                "It is not your turn",
                ephemeral=True,
            )

        letter = "X" if self.view.current_player == self.view.p2 else "O"

        result = self.view.game.update_postion(letter, self.pos)

        if result[0] == "invalid":
            return await interaction.followup.send("Invalid move", ephemeral=True)

        elif result[0] == "win":
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Game Over!",
                    description=f"Yay {self.view.current_player.mention} wins",
                    color=discord.Color.random(),
                )
            )
            await self.view.on_timeout()

        elif result[0] == "draw":
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Game Over!",
                    description="Its a draw gg",
                    color=discord.Color.random(),
                )
            )
            await self.view.on_timeout()

        elif result[0] == "continue":
            if self.view.current_player == self.view.p1:
                self.view.current_player = self.view.p2
            else:
                self.view.current_player = self.view.p1

        await self.view.redraw_buttons()


class TicTacToe2PlayerView(discord.ui.View):
    """View for tic tac toe member vs member mode"""

    def __init__(self, player1: discord.Member, player2: discord.Member):
        self.game = TicTacToeGame()
        self.p1 = player1
        self.p2 = player2

        self.current_player = player2

        super().__init__(timeout=500)

        for pos in range(1, 10):
            self.add_item(TicTacToe2PlayerButton(pos))

    async def redraw_buttons(self):
        for idxa, row in enumerate(self.game.board):
            for idxb, box in enumerate(row):
                if box == FREE_SPACE:
                    continue

                index = (3 * idxa) + idxb
                self.children[index].label = box

        await self.message.edit(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user not in [self.p1, self.p2]:
            await interaction.response.send_message(
                "You are not playing this game",
                ephemeral=True,
            )
            return False

        return True

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)
        await super().on_timeout()

        self.stop()


class TicTacToeAIView(discord.ui.View):
    """View for tic tac toe member vs ai mode"""

    def __init__(self, player):
        self.game = TicTacToeAI()
        self.player = player

        self.current_player = player

        super().__init__(timeout=500)

        for pos in range(1, 10):
            self.add_item(TicTacToeAIButton(pos))

    async def redraw_buttons(self):
        for idxa, row in enumerate(self.game.board):
            for idxb, box in enumerate(row):
                if box == FREE_SPACE:
                    continue

                index = (3 * idxa) + idxb
                self.children[index].label = box

        await self.message.edit(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.current_player:
            await interaction.response.send_message(
                "You are not playing this game",
                ephemeral=True,
            )
            return False

        return True

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True

        await self.message.edit(view=self)
        await super().on_timeout()

        self.stop()


class TicTacToeAIButton(TicTacToe2PlayerButton):
    """
    Class for a single button (out of 9) on the member vs ai mode for tic tac toe
    This will be used by the TicTacToeAIView
    """

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user != self.view.current_player:
            return await interaction.followup.send(
                "It is not your turn",
                ephemeral=True,
            )

        if self.view.current_player == self.view.player:
            result = self.view.game.update_postion("X", self.pos)

        if result[0] == "invalid":
            return await interaction.followup.send("Invalid move", ephemeral=True)

        elif result[0] == "continue":
            if self.view.current_player == "bot":
                self.view.current_player = self.view.player
            else:
                self.view.current_player = "bot"
                result = self.view.game.bot_move("O")

        if result[0] == "win":
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Game Over!",
                    description=f"Yay {self.view.current_player} wins",
                    color=discord.Color.random(),
                )
            )
            await self.view.on_timeout()

        elif result[0] == "draw":
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Game Over!",
                    description="Its a draw gg",
                    color=discord.Color.random(),
                )
            )
            await self.view.on_timeout()

        if self.view.current_player == "bot":
            self.view.current_player = self.view.player

        await self.view.redraw_buttons()
