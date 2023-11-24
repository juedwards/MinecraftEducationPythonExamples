# Block Planner
# A small app to help children transition from 2D to 3D space
# Justin Edwards, Microsoft
# 24 November 2023

import tkinter as tk

def toggle_color(event):
    x, y = event.x, event.y
    x_grid = (x - 50) // 20
    y_grid = (y - 50) // 20

    if 0 <= x_grid < 20 and 0 <= y_grid < 20:
        item = grid_items[y_grid][x_grid]
        current_color = canvas.itemcget(item, "fill")
        new_color = "black" if current_color == "white" else "white"
        canvas.itemconfig(item, fill=new_color)
        update_count()

def reset_grid():
    for row in grid_items:
        for item in row:
            canvas.itemconfig(item, fill="white")
    update_count()

def update_count():
    count = sum(canvas.itemcget(item, "fill") == "black" for row in grid_items for item in row)
    count_var.set(f"Black Squares: {count}")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("BlockPlanner")
root.geometry("500x500")

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

grid_items = []
for i in range(20):
    row_items = []
    for j in range(20):
        x0, y0 = 50 + j * 20, 50 + i * 20
        item = canvas.create_rectangle(x0, y0, x0 + 20, y0 + 20, fill="white")
        row_items.append(item)
    grid_items.append(row_items)

reset_button = tk.Button(root, text="Reset", command=reset_grid)
reset_button.place(x=10, y=10)

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.place(x=80, y=10)

count_var = tk.StringVar()
count_label = tk.Label(root, textvariable=count_var)
count_label.place(x=10, y=470)
update_count()

canvas.bind("<Button-1>", toggle_color)

root.mainloop()
