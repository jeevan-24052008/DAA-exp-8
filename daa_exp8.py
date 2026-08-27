from itertools import permutations
import tkinter as tk
from tkinter import messagebox


def travelling_salesman(cost_matrix):
    """Find the cheapest tour starting and ending at city 0."""
    city_count = len(cost_matrix)
    minimum_cost = float("inf")
    best_tour = None

    for order in permutations(range(1, city_count)):
        tour = (0,) + order + (0,)
        tour_cost = sum(cost_matrix[tour[index]][tour[index + 1]] for index in range(city_count))
        if tour_cost < minimum_cost:
            minimum_cost = tour_cost
            best_tour = tour
    return best_tour, minimum_cost


def read_cost_matrix(city_count):
    rows = matrix_text.get("1.0", tk.END).strip().splitlines()
    if len(rows) != city_count:
        raise ValueError

    matrix = []
    for row_index, row in enumerate(rows):
        values = [int(value) for value in row.split()]
        if len(values) != city_count or any(value < 0 for value in values):
            raise ValueError
        values[row_index] = 0
        matrix.append(values)
    return matrix


def find_best_tour():
    try:
        city_count = int(cities_entry.get())
        if not 2 <= city_count <= 9:
            raise ValueError
        cost_matrix = read_cost_matrix(city_count)
    except ValueError:
        messagebox.showerror(
            "Invalid input",
            "Enter 2 to 9 cities and a square matrix of non-negative whole numbers.\n"
            "Use spaces between values and one row per line.",
        )
        return

    tour, cost = travelling_salesman(cost_matrix)
    city_names = [chr(65 + city) for city in tour]
    route_details = "\n".join(
        f"{city_names[index]} → {city_names[index + 1]}: {cost_matrix[tour[index]][tour[index + 1]]}"
        for index in range(city_count)
    )
    result_label.config(
        text=f"Optimal tour: {' → '.join(city_names)}\nMinimum cost: {cost}\n\nPath details:\n{route_details}"
    )


root = tk.Tk()
root.title("Travelling Salesman Problem")
root.geometry("620x600")
root.resizable(False, False)

tk.Label(root, text="Travelling Salesman Problem", font=("Arial", 17, "bold")).pack(pady=(18, 10))

input_frame = tk.Frame(root)
input_frame.pack()
tk.Label(input_frame, text="Number of cities (2–9):").pack(side="left")
cities_entry = tk.Entry(input_frame, width=8)
cities_entry.pack(side="left", padx=7)
cities_entry.insert(0, "5")

tk.Label(root, text="Cost matrix: use spaces between values and one row per line.").pack(pady=(13, 3))
tk.Label(root, text="The diagonal values are ignored (a city to itself has cost 0).", font=("Arial", 9)).pack()

matrix_text = tk.Text(root, height=7, width=37, font=("Consolas", 11))
matrix_text.pack(pady=6)
matrix_text.insert("1.0", "0 10 8 9 7\n10 0 10 5 6\n8 10 0 8 9\n9 5 8 0 6\n7 6 9 6 0")

tk.Button(root, text="Find Optimal Tour", command=find_best_tour, width=20).pack(pady=12)

result_label = tk.Label(root, text="Click Find Optimal Tour to view the result.", justify="left", font=("Arial", 10))
result_label.pack(padx=20, pady=8, anchor="w")

root.mainloop()
