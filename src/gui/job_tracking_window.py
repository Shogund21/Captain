import tkinter as tk
from tkinter import ttk


class JobTrackingWindow:
    def __init__(self, parent, job_tracker):
        self.frame = ttk.Frame(parent)
        self.job_tracker = job_tracker

        self.create_widgets()

    def create_widgets(self):
        self.company_label = ttk.Label(self.frame, text="Company:")
        self.company_label.pack(pady=5)

        self.company_entry = ttk.Entry(self.frame, width=50)
        self.company_entry.pack(pady=5)

        self.position_label = ttk.Label(self.frame, text="Position:")
        self.position_label.pack(pady=5)

        self.position_entry = ttk.Entry(self.frame, width=50)
        self.position_entry.pack(pady=5)

        self.date_label = ttk.Label(self.frame, text="Date (YYYY-MM-DD):")
        self.date_label.pack(pady=5)

        self.date_entry = ttk.Entry(self.frame, width=50)
        self.date_entry.pack(pady=5)

        self.status_label = ttk.Label(self.frame, text="Status:")
        self.status_label.pack(pady=5)

        self.status_entry = ttk.Entry(self.frame, width=50)
        self.status_entry.pack(pady=5)

        self.add_button = ttk.Button(self.frame, text="Add Application", command=self.add_application)
        self.add_button.pack(pady=10)

        self.applications_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.applications_listbox.pack(pady=5)

        self.load_applications()

    def add_application(self):
        company = self.company_entry.get()
        position = self.position_entry.get()
        date = self.date_entry.get()
        status = self.status_entry.get()
        self.job_tracker.add_application(company, position, date, status)
        self.load_applications()

    def load_applications(self):
        self.applications_listbox.delete(0, tk.END)
        applications = self.job_tracker.get_applications()
        for app in applications:
            self.applications_listbox.insert(tk.END, f"{app[1]} - {app[2]} - {app[3]} - {app[4]}")
