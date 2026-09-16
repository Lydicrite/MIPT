num = 1
for r in range (5):
    for c in range (5):
        if (r + c) % 2 == 0:
            print(f"{'*':>3}", end="")
        else:
            print(f"{num:>3}", end="")
            num += 1
    print()
