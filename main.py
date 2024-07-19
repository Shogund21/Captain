import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.job_tracking import JobApplicationTracker
from src.resume_management import ResumeManager
from src.resume_processing import process_resume
from src.chroma import setup_chroma
from src.utils.api_key_management import load_api_key, setup_logging
import openai
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Captain Job Application Tracker")
        self.root.geometry("800x600")

        setup_logging()
        self.api_key = self.load_api_key()
        openai.api_key = self.api_key

        self.job_tracker = JobApplicationTracker()
        self.resume_manager = ResumeManager()
        self.resume_collection = setup_chroma()

        self.create_widgets()

    def load_api_key(self):
        api_key = load_api_key()
        if not api_key:
            messagebox.showerror("Error", "Failed to load API key.")
            self.root.destroy()
        return api_key

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.job_tracking_frame = ttk.Frame(self.notebook)
        self.resume_management_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.job_tracking_frame, text='Job Tracking')
        self.notebook.add(self.resume_management_frame, text='Resume Management')

        self.create_job_tracking_widgets()
        self.create_resume_management_widgets()

    def create_job_tracking_widgets(self):
        self.company_label = ttk.Label(self.job_tracking_frame, text="Company:")
        self.company_label.pack(anchor=tk.W)
        self.company_entry = ttk.Entry(self.job_tracking_frame)
        self.company_entry.pack(anchor=tk.W)

        self.position_label = ttk.Label(self.job_tracking_frame, text="Position:")
        self.position_label.pack(anchor=tk.W)
        self.position_entry = ttk.Entry(self.job_tracking_frame)
        self.position_entry.pack(anchor=tk.W)

        self.date_label = ttk.Label(self.job_tracking_frame, text="Date (MM/DD/YYYY):")
        self.date_label.pack(anchor=tk.W)
        self.date_entry = ttk.Entry(self.job_tracking_frame)
        self.date_entry.pack(anchor=tk.W)

        self.status_label = ttk.Label(self.job_tracking_frame, text="Status:")
        self.status_label.pack(anchor=tk.W)
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(self.job_tracking_frame, textvariable=self.status_var)
        self.status_combobox['values'] = ("Applied", "Interviewing", "Offered", "Rejected", "Waiting for Call Back")
        self.status_combobox.pack(anchor=tk.W)

        self.add_application_button = ttk.Button(self.job_tracking_frame, text="Add Application", command=self.add_application)
        self.add_application_button.pack(anchor=tk.W)

        self.applications_listbox = tk.Listbox(self.job_tracking_frame, height=10)
        self.applications_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        self.applications_listbox.bind('<Double-1>', self.edit_application)

        self.clear_all_button = ttk.Button(self.job_tracking_frame, text="Clear All", command=self.clear_all_applications)
        self.clear_all_button.pack(anchor=tk.W)

        self.update_applications_listbox()

    def create_resume_management_widgets(self):
        self.resume_file_path_label = ttk.Label(self.resume_management_frame, text="Resume File Path:")
        self.resume_file_path_label.pack(anchor=tk.W)
        self.resume_file_path_entry = ttk.Entry(self.resume_management_frame)
        self.resume_file_path_entry.pack(anchor=tk.W)

        self.upload_resume_button = ttk.Button(self.resume_management_frame, text="Browse and Upload Resume", command=self.upload_resume)
        self.upload_resume_button.pack(anchor=tk.W)

        self.resume_listbox = tk.Listbox(self.resume_management_frame, height=10, width=50)
        self.resume_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.resume_management_frame, orient="vertical", command=self.resume_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.resume_listbox.configure(yscrollcommand=scrollbar.set)

        self.view_resume_button = ttk.Button(self.resume_management_frame, text="View Resume", command=self.view_resume)
        self.view_resume_button.pack(anchor=tk.W)

        self.delete_resume_button = ttk.Button(self.resume_management_frame, text="Delete Resume", command=self.delete_resume)
        self.delete_resume_button.pack(anchor=tk.W)

        self.analyze_resume_button = ttk.Button(self.resume_management_frame, text="Analyze and Enhance Resume", command=self.analyze_and_enhance_resume)
        self.analyze_resume_button.pack(anchor=tk.W)

        self.update_resume_listbox()

    def add_application(self):
        company = self.company_entry.get()
        position = self.position_entry.get()
        date = self.date_entry.get()
        status = self.status_var.get()
        self.job_tracker.add_application(company, position, date, status)
        self.update_applications_listbox()

    def clear_all_applications(self):
        self.job_tracker.clear_all_applications()
        self.update_applications_listbox()

    def edit_application(self, event):
        selected_index = self.applications_listbox.curselection()[0]
        selected_application = self.job_tracker.get_applications()[selected_index]
        new_status = self.status_combobox.get()
        self.job_tracker.update_application_status(selected_application[0], new_status)
        self.update_applications_listbox()

    def upload_resume(self):
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("PDF files", "*.pdf"), ("Word documents", "*.docx"), ("Text files", "*.txt"), ("Markdown files", "*.md")])
        if file_path:
            try:
                self.resume_manager.ingest_resume(file_path)
                messagebox.showinfo("Success", "Resume uploaded and processed successfully!")
                self.update_resume_listbox()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload resume: {str(e)}")

    def update_applications_listbox(self):
        self.applications_listbox.delete(0, tk.END)
        for app in self.job_tracker.get_applications():
            self.applications_listbox.insert(tk.END, f"{app[0]} - {app[1]} - {app[3]}")

    def update_resume_listbox(self):
        self.resume_listbox.delete(0, tk.END)
        try:
            for resume in os.listdir(self.resume_manager.storage_dir):
                self.resume_listbox.insert(tk.END, resume)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update resume list: {str(e)}")

    def view_resume(self):
        selected_indices = self.resume_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select a resume to view.")
            return

        selected_resume = self.resume_listbox.get(selected_indices[0])
        resume_path = os.path.join(self.resume_manager.storage_dir, selected_resume)

        if not os.path.exists(resume_path):
            messagebox.showerror("Error", f"The file {selected_resume} does not exist.")
            return

        view_window = tk.Toplevel(self.root)
        view_window.title(f"Viewing: {selected_resume}")
        view_window.geometry("600x400")

        text_widget = tk.Text(view_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill=tk.BOTH)

        try:
            with open(resume_path, 'r', encoding='utf-8') as file:
                content = file.read()
            text_widget.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {str(e)}")
            view_window.destroy()

    def delete_resume(self):
        selected_indices = self.resume_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select a resume to delete.")
            return

        selected_resume = self.resume_listbox.get(selected_indices[0])
        resume_path = os.path.join(self.resume_manager.storage_dir, selected_resume)

        if not os.path.exists(resume_path):
            messagebox.showerror("Error", f"The file {selected_resume} does not exist.")
            return

        try:
            os.remove(resume_path)
            messagebox.showinfo("Success", f"{selected_resume} deleted successfully!")
            self.update_resume_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete the resume: {str(e)}")

    def analyze_and_enhance_resume(self):
        selected_indices = self.resume_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select a resume to analyze.")
            return

        selected_index = selected_indices[0]
        selected_resume = self.resume_listbox.get(selected_index)
        resume_path = os.path.join(self.resume_manager.storage_dir, selected_resume)

        if not os.path.exists(resume_path):
            messagebox.showerror("Error", f"The file {selected_resume} does not exist.")
            return

        try:
            application = self.job_tracker.get_applications()[selected_index]
            company = application[0]
            position = application[1]

            with open(resume_path, 'r', encoding='utf-8') as file:
                resume_content = file.read()

            prompt = f"Analyze this resume and enhance it for the job application at {company} for the position of {position}. Here is the resume:\n\n{resume_content}"

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that helps enhance resumes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )

            enhanced_resume_content = response.choices[0]['message']['content'].strip()

            with open(resume_path, 'w', encoding='utf-8') as file:
                file.write(enhanced_resume_content)

            messagebox.showinfo("Success", "Resume analyzed and enhanced successfully!")
            self.update_resume_listbox()
        except IndexError:
            messagebox.showerror("Error", "Failed to retrieve application details. Please make sure the selected resume corresponds to a valid application.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze and enhance the resume: {str(e)}")

def main():
    print("Starting main...")
    root = tk.Tk()
    print("Initializing MainWindow...")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
