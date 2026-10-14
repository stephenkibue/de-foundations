eggs_collected = int(input("How many eggs were collected today? "))
eggs_per_tray = 30

full_trays = eggs_collected // eggs_per_tray
eggs_left = eggs_collected % eggs_per_tray

price_per_tray = int(input("What is the price per tray in shillings? "))
#eggs_left do not earn anything today;they are held back to be sold tomorrow in full rays.
revenue= full_trays * price_per_tray
print(f'Today, we collected {eggs_collected} eggs, which filled {full_trays} trays and left {eggs_left} eggs. The revenue from selling the full trays is {revenue:,} shillings.')
