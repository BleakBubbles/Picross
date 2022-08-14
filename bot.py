#import necessary modules
import hikari
import lightbulb
import logging
import random

# load file with token inside, in read mode
token = open("token.txt", "r")
# read  token from the file
t = token.read()

# set up bot with its token and logging configuration
bot = lightbulb.BotApp(token=t,logs=logging.INFO)

# print a message to the console once the bot has gone online
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("Picross is up and running.")

# set up the picross command with its parameters, name, and description
@bot.command
@lightbulb.option('width', 'width of the grid', int, required=True, min_value=2, max_value=10)
@lightbulb.option('length', 'length of the grid', int, required=True, min_value=2, max_value=10)
@lightbulb.command('picross', 'generates a picross board of given side lengths.')
@lightbulb.implements(lightbulb.SlashCommand)
async def picross(context: lightbulb.Context):
    l = context.options.length
    w = context.options.width

    # define a 2D array of 0s to represent the picross grid
    layout = [[0 for i in range(l)] for j in range(w)]
    # define a counter to track the number of 'X' squares
    c = 0
    # turn n squares into 'X' squares where n is equal to the integer division of the area of the board by 2
    while c < l * w / 2:
        # generate random coordinates and turn the square at that coordinate into an 'X'
        y = random.randint(0, w-1)
        x = random.randint(0, l-1)
        # if the coordinate is not already an 'X', turn it into one
        if layout[y][x] != 1:
            layout[y][x] = 1
            c += 1
    
    # list of emoji names for convenience
    emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']

    # declare an empty 2D array with l arrays. This will store the square numbers for vertical columns
    vnums = [[] for i in range(l)]
    # loop through each column
    for i in range(l):
        # declare a counter variable and set it equal to 0
        s = 0
        # loop through each element in the column
        for j in range(w):
            # if the element is a correct square, add 1 to the counter
            if layout[j][i] == 0: s += 1
            # if the element is an incorrect square or if the element is the last one in the column, add the counter to the 2D array and reset it
            if (layout[j][i] == 1 or j == (w-1)) and s > 0: 
                vnums[i].append(emojis[s])
                s = 0
        # if the 2D array is empty, then the entire column is incorrect and a :zero: is added
        if not bool(vnums[i]): vnums[i].append(emojis[0])
    # determine the maximum length of counters added to each column. This will be useful later for printing
    vmax = max(len(i) for i in vnums)

    # repeat the above process but for horizontal rows instead
    hnums = [[] for i in range(w)]
    for h, i in enumerate(layout):
        s = 0
        for k, j in enumerate(i):
            if j == 0: s += 1
            if (j == 1 or k == (l-1)) and s > 0: 
                hnums[h].append(emojis[s])
                s = 0
        if not bool(hnums[h]): hnums[h].append(emojis[0])
    hmax = max(len(i) for i in hnums)

    # declare a 2D array representing the layout above the picross grid. By default, it will be filled with filler squares
    vlayout = [[':black_large_square:' for i in range(vmax)] for j in range(l)]

    # set the end of each layout column to the corresponding square number column, accounting for size differences using splices and vmax
    for i in range(l):
        vlayout[i] = vlayout[i][:vmax-len(vnums[i])] + [j for j in vnums[i]]

    # rotate vlayout 90 degrees clockwise so that it is printed in the correct orientation
    vlayout = [list(i) for i in list(zip(*vlayout))]

    # add a n filler squares at the beginning of each vlayout row, where n is the maximum number of horizontal square numbers
    for i in vlayout:
        for j in range(hmax):
            i.insert(0,':black_large_square:')

    # repeat the above process but for the horizontal layout instead
    hlayout = [[':black_large_square:' for i in range(hmax)] for j in range(w)]

    # as a difference from the vertical layout, the actual picross grid must be added row by row to each row of the horizontal layout
    for i in range(w):
        hlayout[i] = hlayout[i][:hmax-len(hnums[i])] + [j for j in hnums[i]] + ['||:x:||' if k == 1 else '||:green_square:||' for k in layout[i]]
    
    # create the board by joining the elements of the vertical layout, the elements of the horizontal layout, and the layouts themselves
    # board = '\n'.join(['\n'.join(''.join(i) for i in vlayout), '\n'.join(''.join(j) for j in hlayout)]) 
    
    # combine every line to be printed into one list called board
    board = [''.join(i) + '‎' for i in vlayout] + [''.join(i) + '‎' for i in hlayout]
    lines = len(board)
    # declare a list called boardprint to store the lines to be printed
    boardprint = []
    # boardprint will contain the lines to be printed, two at a time. Hence, whether or not there is an even or odd number of lines
    # needs to be accounted for
    if lines % 2 == 0:
        for i in range(0, lines, 2):
            boardprint.append('\n'.join([board[i], board[i+1]]))
    else:
        boardprint.append(board[0])
        for i in range(1, lines, 2):
            boardprint.append('\n'.join([board[i], board[i+1]]))

    # reply to the user with the first line to be printed and send the rest of the lines in succession
    await context.respond(boardprint[0])
    for i in boardprint:
        await bot.rest.create_message(context.channel_id, i)

#set up the joy command with name and description
@bot.command
@lightbulb.command('joy','generates the joy emoji.')
@lightbulb.implements(lightbulb.SlashCommand)
async def joy(context:lightbulb.Context):
    # print the joy emoji
    await context.respond('''⬛⬛⬛⬛🟨🟨🟨🟨🟨⬛⬛⬛⬛
⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛
⬛⬛🟨⬛🟨🟨🟨🟨🟨⬛🟨⬛⬛
⬛🟨⬛🟨🟨🟨🟨🟨🟨🟨⬛🟨⬛
⬛🟨🟨⬛⬛🟨🟨🟨⬛⬛🟨🟨⬛
⬛🟨⬛🟦🟨⬛🟨⬛🟨🟦⬛🟨⬛
⬛🟦🟦🟦🟨🟨🟨🟨🟨🟦🟦🟦⬛
🟦🟦🟦🟦⬜⬜⬜⬜⬜🟦🟦🟦🟦
🟦🟦🟦🟦⬛⬛⬛⬛⬛🟦🟦🟦🟦
⬛🟦🟦🟨🟨⬛⬛⬛🟨🟨🟦🟦⬛
⬛⬛⬛⬛🟨🟨🟨🟨🟨⬛⬛⬛⬛''')


# set up the github command with name and description
@bot.command
@lightbulb.command('github','provides a link to the bot\'s GitHub repository.')
@lightbulb.implements(lightbulb.SlashCommand)
async def github(context:lightbulb.Context):
    # print the link to the GitHub
    await context.respond('https://github.com/BleakBubbles/Picross')

# run the bot
bot.run()