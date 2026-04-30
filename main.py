import runpy
from clean_data import load_and_clean_data
from relationships import relPlot

print("\n\n--------------------------")
print("CS_2300 - Final Project")
print("--------------------------\n")

df_clean = None

while True:
    print("\nCONTROL PANEL")
    print("1. Clean data")
    print("2. Run Dist_1 visualization")
    print("3. Run Dist_2 visualization")
    print("4. Run relationships visualization")
    print("5. Run all visualizations")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        df_clean = load_and_clean_data()

    elif choice == "2":
        if df_clean is None:
            df_clean = load_and_clean_data()

        runpy.run_path("Dist_1.py")

    elif choice == "3":
        if df_clean is None:
            df_clean = load_and_clean_data()

        runpy.run_path("Dist_2.py", init_globals={"df_clean": df_clean})

    elif choice == "4":
        fig = relPlot()
        fig.show()

    elif choice == "5":
        if df_clean is None:
            df_clean = load_and_clean_data()

        runpy.run_path("Dist_1.py")
        runpy.run_path("Dist_2.py", init_globals={"df_clean": df_clean})

        fig = relPlot()
        fig.show()

    elif choice == "6":
        print("\nEND OF PROGRAM\n")
        break

    else:
        print("Invalid choice. Try again.")
