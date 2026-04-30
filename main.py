from vis_code.clean_data import load_and_clean_data
from vis_code.Dist_1 import dist1
from vis_code.Dist_2 import dist2
from vis_code.relationships import relPlot
from vis_code.Agg import agg

print("--------------------------")
print("CS_2300 - Final Project")
print("--------------------------\n")

print("Cleaning data:")
df_clean = load_and_clean_data()

running = True

while running:
    print("\nCONTROL PANEL")
    print("1. Run crashes by severity visualization")
    print("2. Run crashes by hour distribution visualization")
    print("3. Run relationships visualization")
    print("4. Run aggregated crashes by borough visualization")
    print("5. Run all visualizations")
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
        agg(df_clean)

    elif choice == "5":
        dist1(df_clean)
        dist2(df_clean)
        fig = relPlot(df_clean)
        fig.show()
        agg(df_clean)

    elif choice == "0":
        print("Goodbye.")
        running = False

    else:
        print("Invalid choice. Try again.")