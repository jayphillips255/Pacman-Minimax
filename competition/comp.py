import game, pacman
import multiAgents, multiAgents2, ghostAgents
import graphicsDisplay
import layout
import helperFuncs # This is our own file, not from Berkley


depth = 3 # But try 3'n stuff

layoutText = helperFuncs.getLayoutString('./layouts/originalClassic.lay')
ourLayout = layout.Layout(layoutText) # But consider 'smallClassic', 'contestClassic' and 'minimaxClassic'

# Define our agents
# Making these Reflex agents for now
jaysAgent = multiAgents.AlphaBetaAgent(multiAgents.MultiAgentSearchAgent(game.Agent(0)))
jessesAgent = multiAgents2.ExpectimaxAgent(multiAgents2.MultiAgentSearchAgent(game.Agent(1)))
ourAgents = [jaysAgent, jessesAgent]

# Define our ghost agents
# We have one directional ghost and one random ghost
ghost1 = ghostAgents.DirectionalGhost(game.Agent(2))
ghost2 = ghostAgents.RandomGhost(game.Agent(3))
ourGhosts = [ghost1, ghost2]

display = graphicsDisplay.PacmanGraphics()
h = 0 # This line is just to catach the debugger with a breakpoint
numGames = 1
record = False

pacman.runGames(ourLayout, ourAgents, ourGhosts, display, numGames, record, numTraining = 0, catchExceptions=False, timeout=30)


# Initialize the competition
# if (numGames-numTraining) > 0:
#     s = [game.state.getScore() for game in games]
#     wins = [game.state.isWin() for game in games]
#     winRate = wins.count(True)/ float(len(wins))
#     print('Average Score:', sum(scores) / float(len(scores)))
#     print('Scores:       ', ', '.join([str(score) for score in scores]))
#     print('Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate))
#     print('Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins]))
