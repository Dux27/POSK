import main
import matplotlib.pyplot as plt


def simpleAnalysis(reaction_times):
    average = sum(reaction_times) / len(reaction_times)
    best = min(reaction_times)

    main.screen.fill(main.BACKGROUND_COLOR)
    main.display_text("Wyniki:", -50)
    main.display_text(f"Średni czas: {average:.3f} s", 0)
    main.display_text(f"Najlepszy czas: {best:.3f} s", 50)
    
    
def linearGraph(reaction_times):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(reaction_times) + 1), reaction_times, marker='o', color='b')
    plt.title("Czas reakcji w poszczególnych próbach")
    plt.xlabel("Numer próby")
    plt.ylabel("Czas reakcji (s)")
    plt.grid(True)
    plt.show()