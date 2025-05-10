import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "tarefas.json"

class TaskManager:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Tarefas")

        self.tasks = []
        self.load_tasks()

        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        self.task_entry = tk.Entry(self.frame, width=40)
        self.task_entry.grid(row=0, column=0, padx=5)
        self.add_button = tk.Button(self.frame, text="Adicionar", command=self.add_task)
        self.add_button.grid(row=0, column=1)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        self.task_listbox.bind("<Double-1>", self.toggle_task_done)

        self.remove_button = tk.Button(self.frame, text="Remover Selecionada", command=self.remove_task)
        self.remove_button.grid(row=2, column=0, columnspan=2)

        self.refresh_task_listbox()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "done": False})
            self.task_entry.delete(0, tk.END)
            self.refresh_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Aviso", "A tarefa não pode estar vazia.")

    def toggle_task_done(self, event):
        index = self.task_listbox.curselection()
        if index:
            idx = index[0]
            self.tasks[idx]["done"] = not self.tasks[idx]["done"]
            self.refresh_task_listbox()
            self.save_tasks()

    def remove_task(self):
        index = self.task_listbox.curselection()
        if index:
            idx = index[0]
            del self.tasks[idx]
            self.refresh_task_listbox()
            self.save_tasks()

    def refresh_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = f"[{'✓' if task['done'] else ' '}] {task['text']}"
            self.task_listbox.insert(tk.END, display_text)

    def save_tasks(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()