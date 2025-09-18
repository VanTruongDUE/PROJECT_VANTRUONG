import random
user_wins = 0
computer_wins = 0
lc = ["Búa", "Bao", "Kéo"]
while True:
    bot = random.choice(lc)
    user = input(" Kéo/Búa/Bao hoặc chọn T để thoát: ")
    if user.lower() == "t":
        break
    if user in lc :
        if user == bot :
            print("DRAW")
        elif user == "Búa" and bot == "Bao":
            print("Human Win")
            user_wins += 1
        elif user == "Kéo" and bot == "Bao":
            print("Human Win")
            user_wins += 1
        elif user == "Bao" and bot == "Kéo":
            print("Human Win")
            user_wins += 1
        else:
            print("Bot Win")
            computer_wins += 1

    else:
        continue
print("You won", user_wins, "times.")
print("The computer won", computer_wins, "times.")
print("Goodbye!")