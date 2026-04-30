from vis_code.clean_data import load_and_clean_data
from vis_code.Dist_1 import dist1
from vis_code.Dist_2 import dist2
from vis_code.relationships import relPlot

print("\n\n--------------------------")
print("CS_2300 - Final Project")
print("--------------------------\n")

print("Cleaning data...")
df_clean = load_and_clean_data()

while True:
    print("\nCONTROL PANEL")
    print("1. Run Dist_1 visualization")
    print("2. Run Dist_2 visualization")
    print("3. Run relationships visualization")
    print("4. Run all visualizations")
    print("0. Quit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        dist1(df_clean)

    elif choice == "2":
        dist2(df_clean)

    elif choice == "3":
        fig = relPlot(df_clean)
        fig.show()

    elif choice == "4":
        dist1(df_clean)
        dist2(df_clean)
        fig = relPlot(df_clean)
        fig.show()

    elif choice == "0":
        print("\nEND OF PROGRAM\n")
        break

    else:
        print("Invalid choice. Try again.")