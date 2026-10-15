# eggs = int(input("How many eggs were collected? "))
# birds = int(input("How many birds are in the flock? "))

birds= 1200

day_number = 1  
total_eggs = 0  
good_days = 0
watch_days = 0
act_now_days = 0

print("Enter dayly eggs. Type 'done' when finished.")
while True:
    # Get the number of eggs for the current day
    entry = input(f"Day {day_number} eggs: ")
    #check for the break immediately, before anything else
    if entry == "done":
        break
    eggs = int(entry)
    rate = eggs / birds

    # Classify the rate
    if rate >= 0.80:
        label = "good"
        good_days= good_days + 1
    elif rate >= 0.60:
        label = "watch"
        watch_days = watch_days + 1
    else:
        label = "act now"
        act_now_days = act_now_days + 1

    #turn the decimal rate into a percentage
    rate_pct = rate * 100

    #print the results(using .1f to get one decimal place)
    print(f"Day {day_number}: {eggs} eggs, {rate_pct:.1f}%", {label})
# If it's the very first day, automatically crown it the champion
    if day_number == 1:
        best_eggs = eggs
        best_day = day_number
        worst_eggs = eggs
        worst_day = day_number
    else:
        if eggs > best_eggs:
            best_eggs = eggs
            best_day = day_number
        
    # 3. Check if this day is the new lowest
        if eggs < worst_eggs:
            worst_eggs = eggs
            worst_day = day_number

    total_eggs = total_eggs + eggs  # 2. Add to the accumulator inside the loop
    day_number = day_number + 1

# figure out how many days were actually entered
days = day_number - 1
if days == 0:
    print("\nNo data entered. cannot calculate statistics.")
else:
    average_eggs = total_eggs / days
    total_bird_days = birds * days
    weekly_rate = total_eggs / total_bird_days

# Reuse the same logic to classify the week's overall rate
    if weekly_rate >= 0.80:
        weekly_label = "good"
    elif weekly_rate >= 0.60:
            weekly_label = "watch"
    else:
        weekly_label = "act now"

    weekly_rate_pct = weekly_rate * 100

#print the final summary
    print("\n--- Weekly Summary ---")
    print(f"Total eggs: {total_eggs}")
    print(f"Average eggs per day: {average_eggs:.1f}")
    print(f"Weekly laying rate: {weekly_rate_pct:.1f}%, {weekly_label}")
    print(f"Best day: Day {best_day} with {best_eggs} eggs")
    print(f"Worst day: Day {worst_day} with {worst_eggs} eggs")
    print(f"Good days: {good_days}, Watch days: {watch_days}, Act now days: {act_now_days}")