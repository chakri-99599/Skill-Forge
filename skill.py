import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class SkillForgeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ SkillForge – Personal Skill Tracker")
        self.geometry("950x600")
        self.resizable(False, False)
        self.data = load_data()
        self.edit_index = None

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Frame: Form
        form = ttk.LabelFrame(self, text="Add / Edit Skill", padding=10)
        form.pack(fill="x", padx=10, pady=5)

        ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = ttk.Entry(form)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Tags:").grid(row=1, column=0, padx=5, pady=5)
        self.tags_entry = ttk.Entry(form)
        self.tags_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Status:").grid(row=1, column=2, padx=5, pady=5)
        self.status_combo = ttk.Combobox(form, values=["Beginner", "Intermediate", "Advanced"], state="readonly")
        self.status_combo.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Progress %:").grid(row=2, column=0, padx=5, pady=5)
        self.progress_entry = ttk.Entry(form)
        self.progress_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Target Date:").grid(row=2, column=2, padx=5, pady=5)
        self.date_entry = ttk.Entry(form)
        self.date_entry.grid(row=2, column=3, padx=5, pady=5)

        self.favorite_var = tk.BooleanVar()
        ttk.Checkbutton(form, text="⭐ Favorite", variable=self.favorite_var).grid(row=2, column=4, padx=5)

        ttk.Button(form, text="Save", command=self.save_skill).grid(row=3, column=1, pady=8)
        ttk.Button(form, text="Update", command=self.update_skill).grid(row=3, column=2, pady=8)
        ttk.Button(form, text="Clear", command=self.clear_form).grid(row=3, column=3, pady=8)

        # Frame: Search
        search_frame = ttk.LabelFrame(self, text="Search / Filter", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search Name:").grid(row=0, column=0, padx=5)
        self.search_name = ttk.Entry(search_frame)
        self.search_name.grid(row=0, column=1, padx=5)

        ttk.Label(search_frame, text="Category:").grid(row=0, column=2, padx=5)
        self.search_category = ttk.Entry(search_frame)
        self.search_category.grid(row=0, column=3, padx=5)

        ttk.Label(search_frame, text="Status:").grid(row=0, column=4, padx=5)
        self.filter_status = ttk.Combobox(search_frame, values=["", "Beginner", "Intermediate", "Advanced"], state="readonly")
        self.filter_status.grid(row=0, column=5, padx=5)

        ttk.Button(search_frame, text="Filter", command=self.filter_data).grid(row=0, column=6, padx=5)
        ttk.Button(search_frame, text="Reset", command=self.refresh_table).grid(row=0, column=7, padx=5)
        ttk.Button(search_frame, text="📊 Show Chart", command=self.show_pie_chart).grid(row=0, column=8, padx=5)

        # Frame: Table
        table_frame = ttk.LabelFrame(self, text="Skills", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("name", "category", "status", "progress", "tags", "date", "favorite")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        ttk.Button(self, text="Delete", command=self.delete_skill).pack(side="left", padx=20, pady=10)
        ttk.Button(self, text="Explore Suggestions 🌍", command=self.show_explore).pack(side="right", padx=20, pady=10)

    def save_skill(self):
        skill = {
            "name": self.name_entry.get().strip(),
            "category": self.category_entry.get().strip(),
            "tags": [t.strip() for t in self.tags_entry.get().split(",") if t.strip()],
            "status": self.status_combo.get(),
            "progress": int(self.progress_entry.get() or 0),
            "target_date": self.date_entry.get().strip(),
            "favorite": self.favorite_var.get()
        }

        if not skill["name"] or not skill["category"] or not skill["status"]:
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        self.data.append(skill)
        save_data(self.data)
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Saved", "Skill added successfully.")

    def update_skill(self):
        if self.edit_index is None:
            messagebox.showwarning("Select", "Select a skill to update.")
            return

        skill = self.data[self.edit_index]
        skill.update({
            "name": self.name_entry.get().strip(),
            "category": self.category_entry.get().strip(),
            "tags": [t.strip() for t in self.tags_entry.get().split(",") if t.strip()],
            "status": self.status_combo.get(),
            "progress": int(self.progress_entry.get() or 0),
            "target_date": self.date_entry.get().strip(),
            "favorite": self.favorite_var.get()
        })

        save_data(self.data)
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Updated", "Skill updated successfully.")

    def delete_skill(self):
        if not self.tree.selection():
            messagebox.showwarning("Select", "Select a skill to delete.")
            return
        index = self.tree.index(self.tree.selection()[0])
        confirm = messagebox.askyesno("Confirm", "Delete this skill?")
        if confirm:
            self.data.pop(index)
            save_data(self.data)
            self.refresh_table()

    def refresh_table(self, filtered=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        display_data = filtered or self.data
        for skill in display_data:
            fav = "⭐" if skill.get("favorite") else ""
            self.tree.insert("", "end", values=(
                skill["name"], skill["category"], skill["status"], 
                f"{skill['progress']}%", ", ".join(skill["tags"]),
                skill["target_date"], fav
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        index = self.tree.index(selected[0])
        skill = self.data[index]
        self.edit_index = index

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, skill["name"])
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, skill["category"])
        self.tags_entry.delete(0, tk.END)
        self.tags_entry.insert(0, ", ".join(skill["tags"]))
        self.status_combo.set(skill["status"])
        self.progress_entry.delete(0, tk.END)
        self.progress_entry.insert(0, skill["progress"])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, skill["target_date"])
        self.favorite_var.set(skill["favorite"])

    def clear_form(self):
        self.edit_index = None
        for e in [self.name_entry, self.category_entry, self.tags_entry, self.progress_entry, self.date_entry]:
            e.delete(0, tk.END)
        self.status_combo.set("")
        self.favorite_var.set(False)

    def filter_data(self):
        name_query = self.search_name.get().lower().strip()
        category_query = self.search_category.get().lower().strip()
        status_filter = self.filter_status.get()

        filtered = self.data
        if name_query:
            filtered = [s for s in filtered if name_query in s["name"].lower()]
        if category_query:
            filtered = [s for s in filtered if category_query in s["category"].lower()]
        if status_filter:
            filtered = [s for s in filtered if s["status"] == status_filter]

        if not filtered:
            self.refresh_table([])
            messagebox.showinfo("No Results", "No matching skills found.")
            return

        self.refresh_table(filtered)

    def show_explore(self):
        suggestions = [
            {"name": "Machine Learning", "category": "AI", "status": "Intermediate"},
            {"name": "Web Development", "category": "Programming", "status": "Beginner"},
            {"name": "Cybersecurity", "category": "IT", "status": "Intermediate"},
            {"name": "Cloud Computing", "category": "Technology", "status": "Advanced"},
            {"name": "Data Analysis", "category": "Data Science", "status": "Intermediate"},
            {"name": "React.js", "category": "Frontend", "status": "Beginner"},
            {"name": "Node.js", "category": "Backend", "status": "Intermediate"},
            {"name": "SQL", "category": "Database", "status": "Intermediate"},
            {"name": "Docker", "category": "DevOps", "status": "Advanced"},
            {"name": "Kubernetes", "category": "DevOps", "status": "Advanced"},
        ]

        win = tk.Toplevel(self)
        win.title("🌍 Explore Skill Suggestions")
        win.geometry("600x400")

        cols = ("name", "category", "status")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col.title())
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True)

        for s in suggestions:
            tree.insert("", "end", values=(s["name"], s["category"], s["status"]))

        def add_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select", "Select a skill to add.")
                return
            values = tree.item(selected[0], "values")
            new_skill = {
                "name": values[0],
                "category": values[1],
                "status": values[2],
                "tags": [],
                "progress": 0,
                "target_date": "",
                "favorite": False
            }
            self.data.append(new_skill)
            save_data(self.data)
            self.refresh_table()
            messagebox.showinfo("Added", f"Skill '{values[0]}' added successfully.")

        ttk.Button(win, text="Add Selected Skill", command=add_selected).pack(pady=10)

    def show_pie_chart(self):
        if not self.data:
            messagebox.showinfo("No Data", "No skills available to show chart.")
            return

        status_counts = {}
        for s in self.data:
            status = s.get("status", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1 

        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(status_counts.values(), labels=status_counts.keys(), autopct="%1.1f%%", startangle=90)
        ax.set_title("Skill Progress Overview")

        chart_win = tk.Toplevel(self)
        chart_win.title("📊 Skill Distribution")
        chart_win.geometry("500x450")

        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
if __name__ == "__main__":
    app = SkillForgeApp()
    app.mainloop()
