import hikari
import lightbulb
import logging
import random

token = open("token.txt", "r")
t = token.read()

bot = lightbulb.BotApp(token=t,logs=logging.INFO)

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("Picross is up and running.")

@bot.command
@lightbulb.option('width', 'width of the grid', int, required=True, min_value=2, max_value=10)
@lightbulb.option('length', 'length of the grid', int, required=True, min_value=2, max_value=10)
@lightbulb.command('picross', 'generates a picross board of given side lengths.')
@lightbulb.implements(lightbulb.SlashCommand)
async def picross(context: lightbulb.Context):
    l = context.options.length
    w = context.options.width

    layout = [[0 for i in range(l)] for j in range(w)]
    c = 0
    while c < l * w / 2:
        y = random.randint(0, w-1)
        x = random.randint(0, l-1)
        if layout[y][x] != 1:
            layout[y][x] = 1
            c += 1
    
    emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']

    vnums = [[] for i in range(l)]
    for i in range(l):
        s = 0
        for j in range(w):
            if layout[j][i] == 0: s += 1
            if (layout[j][i] == 1 or j == (w-1)) and s > 0: 
                vnums[i].append(emojis[s])
                s = 0
        if not bool(vnums[i]): vnums[i].append(emojis[0])
    vmax = max(len(i) for i in vnums)

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

    vlayout = [[':black_large_square:' for i in range(vmax)] for j in range(l)]

    for i in range(l):
        vlayout[i] = vlayout[i][:vmax-len(vnums[i])] + [j for j in vnums[i]]

    vlayout = [list(i) for i in list(zip(*vlayout))]

    for i in vlayout:
        for j in range(hmax):
            i.insert(0,':black_large_square:')

    hlayout = [[':black_large_square:' for i in range(hmax)] for j in range(w)]

    for i in range(w):
        hlayout[i] = hlayout[i][:hmax-len(hnums[i])] + [j for j in hnums[i]] + ['||:x:||' if k == 1 else '||:green_square:||' for k in layout[i]]
    
    board = '\n'.join(['\n'.join(''.join(i) for i in vlayout), '\n'.join(''.join(j) for j in hlayout)]) 
    
    await context.respond(''.join(vlayout[0]) + '‎')
    for i in range(1, len(vlayout)):
        await bot.rest.create_message(context.channel_id, ''.join(vlayout[i]) + '‎')
    for i in hlayout:
        await bot.rest.create_message(context.channel_id, ''.join(i) + '‎')

@bot.command
@lightbulb.command('joy','generates the joy emoji.')
@lightbulb.implements(lightbulb.SlashCommand)
async def joy(context:lightbulb.Context):
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

@bot.command
@lightbulb.command('github','provides a link to the bot\'s Github repository.')
@lightbulb.implements(lightbulb.SlashCommand)
async def github(context:lightbulb.Context):
    await context.respond('https://github.com/BleakBubbles/Picross')

bot.run()