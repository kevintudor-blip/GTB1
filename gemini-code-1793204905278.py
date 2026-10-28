import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class SeaTurtleTokenBoard:

  def __init__(self, root):
    self.root = root
    self.root.title("George's Sea Turtle Token Board")
    self.root.geometry("620x780")
    self.root.configure(bg="#E0F7FA")  # Ocean light teal background

    # State Variables
    self.tokens = 0
    self.max_tokens = 5
    self.reward_var = tk.StringVar(value="YouTube Video")
    self.awarder_var = tk.StringVar(value="Teacher")
    self.activity_history = []
    self.data_file = "george_token_board_data.json"

    # UI Setup
    self.setup_styles()
    self.create_widgets()
    self.load_data()
    self.render_slots()

  def setup_styles(self):
    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure("TFrame", background="#E0F7FA")
    self.style.configure(
        "Header.TLabel",
        font=("Segoe UI", 18, "bold"),
        foreground="#004D40",
        background="#E0F7FA",
    )
    self.style.configure(
        "SubHeader.TLabel",
        font=("Segoe UI", 11),
        foreground="#00695C",
        background="#E0F7FA",
    )
    self.style.configure(
        "Action.TButton", font=("Segoe UI", 11, "bold"), padding=8
    )

  def create_widgets(self):
    # Header Section
    header_frame = ttk.Frame(self.root)
    header_frame.pack(fill="x", padx=20, pady=(15, 5))

    title_label = ttk.Label(
        header_frame,
        text="🐢 George's Token Board",
        style="Header.TLabel",
    )
    title_label.pack()

    subtitle = ttk.Label(
        header_frame,
        text="Collect 5 sea turtles to earn your reward!",
        style="SubHeader.TLabel",
    )
    subtitle.pack()

    # Reward Selection Section
    reward_frame = tk.LabelFrame(
        self.root,
        text=" Working For (Reward Target) ",
        bg="#B2EBF2",
        fg="#004D40",
        font=("Segoe UI", 11, "bold"),
        padx=15,
        pady=10,
    )
    reward_frame.pack(fill="x", padx=20, pady=10)

    reward_presets = ["YouTube Video", "A turtle", "Tinkercad", "Walk"]
    preset_btn_frame = tk.Frame(reward_frame, bg="#B2EBF2")
    preset_btn_frame.pack(fill="x", pady=(0, 5))

    for item in reward_presets:
      btn = tk.Button(
          preset_btn_frame,
          text=item,
          font=("Segoe UI", 9, "bold"),
          bg="#00897B",
          fg="white",
          activebackground="#00695C",
          activeforeground="white",
          command=lambda r=item: self.set_reward(r),
      )
      btn.pack(side="left", expand=True, fill="x", padx=2)

    reward_entry = tk.Entry(
        reward_frame,
        textvariable=self.reward_var,
        font=("Segoe UI", 12),
        justify="center",
    )
    reward_entry.pack(fill="x", pady=5)

    # Token Shell Grid Display
    self.tokens_frame = tk.LabelFrame(
        self.root,
        text=" Token Slots ",
        bg="#E0F7FA",
        fg="#004D40",
        font=("Segoe UI", 11, "bold"),
        padx=10,
        pady=10,
    )
    self.tokens_frame.pack(fill="x", padx=20, pady=10)

    self.slot_buttons = []
    for i in range(self.max_tokens):
      btn = tk.Button(
          self.tokens_frame,
          text="🐚\nSlot " + str(i + 1),
          font=("Segoe UI", 14),
          width=8,
          height=3,
          bg="#80DEEA",
          fg="#004D40",
          relief="groove",
          command=lambda idx=i: self.toggle_slot(idx),
      )
      btn.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
      self.tokens_frame.columnconfigure(i, weight=1)
      self.slot_buttons.append(btn)

    # Awarder Selection Section
    awarder_frame = tk.LabelFrame(
        self.root,
        text=" Awarded By ",
        bg="#B2EBF2",
        fg="#004D40",
        font=("Segoe UI", 11, "bold"),
        padx=15,
        pady=10,
    )
    awarder_frame.pack(fill="x", padx=20, pady=5)

    awarder_preset_frame = tk.Frame(awarder_frame, bg="#B2EBF2")
    awarder_preset_frame.pack(fill="x", pady=(0, 5))

    for role in ["Teacher", "Therapist"]:
      btn = tk.Button(
          awarder_preset_frame,
          text=role,
          font=("Segoe UI", 9, "bold"),
          bg="#0288D1",
          fg="white",
          activebackground="#01579B",
          activeforeground="white",
          command=lambda r=role: self.set_awarder(r),
      )
      btn.pack(side="left", expand=True, fill="x", padx=2)

    awarder_entry = tk.Entry(
        awarder_frame,
        textvariable=self.awarder_var,
        font=("Segoe UI", 11),
        justify="center",
    )
    awarder_entry.pack(fill="x")

    # Control Buttons (+1, -1, Reset)
    controls_frame = tk.Frame(self.root, bg="#E0F7FA")
    controls_frame.pack(fill="x", padx=20, pady=10)

    add_btn = tk.Button(
        controls_frame,
        text="➕ Add Token (+1)",
        font=("Segoe UI", 11, "bold"),
        bg="#4CAF50",
        fg="white",
        command=self.add_token,
    )
    add_btn.pack(side="left", expand=True, fill="x", padx=3)

    remove_btn = tk.Button(
        controls_frame,
        text="➖ Remove (-1)",
        font=("Segoe UI", 11, "bold"),
        bg="#FF9800",
        fg="white",
        command=self.remove_token,
    )
    remove_btn.pack(side="left", expand=True, fill="x", padx=3)

    reset_btn = tk.Button(
        controls_frame,
        text="🔄 Reset Board",
        font=("Segoe UI", 11, "bold"),
        bg="#E53935",
        fg="white",
        command=self.reset_board,
    )
    reset_btn.pack(side="left", expand=True, fill="x", padx=3)

    # Activity Log Display
    log_frame = tk.LabelFrame(
        self.root,
        text=" Activity History Log ",
        bg="#E0F7FA",
        fg="#004D40",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=5,
    )
    log_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    self.log_listbox = tk.Listbox(
        log_frame,
        font=("Consolas", 9),
        bg="#FFFFFF",
        fg="#263238",
        selectbackground="#B2EBF2",
    )
    scrollbar = tk.Scrollbar(
        log_frame, orient="vertical", command=self.log_listbox.yview
    )
    self.log_listbox.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    self.log_listbox.pack(side="left", fill="both", expand=True)

  def set_reward(self, value):
    self.reward_var.set(value)
    self.save_data()

  def set_awarder(self, value):
    self.awarder_var.set(value)

  def render_slots(self):
    for i in range(self.max_tokens):
      if i < self.tokens:
        self.slot_buttons[i].config(
            text="🐢\nToken " + str(i + 1),
            bg="#4CAF50",
            fg="white",
            relief="raised",
        )
      else:
        self.slot_buttons[i].config(
            text="🐚\nSlot " + str(i + 1),
            bg="#80DEEA",
            fg="#004D40",
            relief="groove",
        )

  def toggle_slot(self, index):
    if index < self.tokens:
      # Clicked an existing token -> remove down to that slot
      self.tokens = index
      self.log_action(f"Removed token from slot {index + 1}")
    else:
      # Clicked an empty slot -> fill up to that slot
      new_tokens = index + 1
      added_count = new_tokens - self.tokens
      self.tokens = new_tokens
      awarder = self.awarder_var.get() or "Caregiver"
      self.log_action(
          f"Added {added_count} token(s) by {awarder} (Total: {self.tokens}/5)"
      )

    self.render_slots()
    self.check_victory()
    self.save_data()

  def add_token(self):
    if self.tokens < self.max_tokens:
      self.tokens += 1
      awarder = self.awarder_var.get() or "Caregiver"
      self.log_action(f"Added token by {awarder} (Total: {self.tokens}/5)")
      self.render_slots()
      self.check_victory()
      self.save_data()

  def remove_token(self):
    if self.tokens > 0:
      self.tokens -= 1
      self.log_action(f"Removed 1 token (Total: {self.tokens}/5)")
      self.render_slots()
      self.save_data()

  def reset_board(self):
    if messagebox.askyesno(
        "Reset Token Board", "Are you sure you want to reset George's tokens?"
    ):
      self.tokens = 0
      self.log_action("Board reset to 0 tokens.")
      self.render_slots()
      self.save_data()

  def check_victory(self):
    if self.tokens == self.max_tokens:
      reward_name = self.reward_var.get() or "your reward"
      messagebox.showinfo(
          "🎉 GREAT JOB GEORGE! 🎉",
          f"Congratulations, George!\n\nYou earned all 5 Sea Turtle Tokens!\n\n🎁 Time for: {reward_name}!",
      )

  def log_action(self, text):
    timestamp = datetime.now().strftime("%I:%M:%S %p")
    entry = f"[{timestamp}] {text}"
    self.activity_history.insert(0, entry)
    self.log_listbox.insert(0, entry)

  def save_data(self):
    data = {
        "tokens": self.tokens,
        "reward": self.reward_var.get(),
        "awarder": self.awarder_var.get(),
        "history": self.activity_history[:50],  # Keep last 50 logs
    }
    try:
      with open(self.data_file, "w") as f:
        json.dump(data, f, indent=2)
    except Exception as e:
      print(f"Error saving data: {e}")

  def load_data(self):
    if os.path.exists(self.data_file):
      try:
        with open(self.data_file, "r") as f:
          data = json.load(f)
          self.tokens = data.get("tokens", 0)
          self.reward_var.set(data.get("reward", "YouTube Video"))
          self.awarder_var.set(data.get("awarder", "Teacher"))
          self.activity_history = data.get("history", [])

          self.log_listbox.delete(0, tk.END)
          for item in reversed(self.activity_history):
            self.log_listbox.insert(0, item)
      except Exception as e:
        print(f"Error loading data: {e}")


if __name__ == "__main__":
  root = tk.Tk()
  app = SeaTurtleTokenBoard(root)
  root.mainloop()