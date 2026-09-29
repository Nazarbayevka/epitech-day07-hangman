def check_penalties(penalties):
    if penalties >= 12:
        print("You lose!")


number = int(input("Enter the number of penalties: "))
check_penalties(number)
