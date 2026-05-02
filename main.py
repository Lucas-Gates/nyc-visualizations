from vis_code.clean_data import load_and_clean_data
from vis_code.Dist_1 import dist1
from vis_code.Dist_2 import dist2
from vis_code.relationships import relPlot
from vis_code.Agg import agg
from vis_code.Parallel import parallel

print("\n--------------------------")
print("CS_2300 - Final Project")
print("--------------------------\n")

print("Cleaning data (est. 3 minutes):")

df_clean = load_and_clean_data()

running = True

while running:
    print("\nCONTROL PANEL")
    print("1. Run crashes by severity distribution visualization")
    print("2. Run crashes by hour distribution visualization")
    print("3. Run relationships visualization")
    print("4. Run aggregated crashes by borough visualization")
    print("5. Run parallel coordinates visualization")
    print("6. Run all visualizations")
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
        parallel(df_clean)

    elif choice == "6":
        dist1(df_clean)
        dist2(df_clean)
        fig = relPlot(df_clean)
        fig.show()
        agg(df_clean)
        parallel(df_clean)
        
    elif choice == "0":
        print("\n--------------------------")
        print("END OF PROGRAM")
        print("--------------------------\n")
        print("Goodbye.")
        running = False

    else:
        print("Invalid choice. Try again.")