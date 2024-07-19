class MainWindow:
    # ... existing code ...

    def create_resume_management_widgets(self):
        self.resume_file_path_label = ttk.Label(self.resume_management_frame, text="Resume File Path:")
        self.resume_file_path_label.pack(anchor=tk.W)
        self.resume_file_path_entry = ttk.Entry(self.resume_management_frame)
        self.resume_file_path_entry.pack(anchor=tk.W)

        self.upload_resume_button = ttk.Button(self.resume_management_frame, text="Browse and Upload Resume", command=self.upload_resume)
        self.upload_resume_button.pack(anchor=tk.W)

        self.summarize_resume_button = ttk.Button(self.resume_management_frame, text="Summarize Resume", command=self.summarize_resume)
        self.summarize_resume_button.pack(anchor=tk.W)

        self.generate_cover_letter_button = ttk.Button(self.resume_management_frame, text="Generate Cover Letter", command=self.generate_cover_letter)
        self.generate_cover_letter_button.pack(anchor=tk.W)

        self.delete_resume_button = ttk.Button(self.resume_management_frame, text="Delete Resume", command=self.delete_resume)
        self.delete_resume_button.pack(anchor=tk.W)

    # ... existing code ...

    def summarize_resume(self):
        selected_index = self.applications_listbox.curselection()
        if selected_index:
            selected_application = self.job_tracker.get_applications()[selected_index[0]]
            app_id = selected_application[0]
            resume_path = self.resumes.get(app_id)
            if resume_path:
                with open(resume_path, 'r') as file:
                    content = file.read()
                summary = summarize_resume(content, api_key='YOUR_OPENAI_API_KEY')
                messagebox.showinfo("Resume Summary", summary)
            else:
                messagebox.showerror("Error", "No resume uploaded for this application.")
        else:
            messagebox.showerror("Error", "Please select an application to summarize the resume.")

    def generate_cover_letter(self):
        selected_index = self.applications_listbox.curselection()
        if selected_index:
            selected_application = self.job_tracker.get_applications()[selected_index[0]]
            app_id = selected_application[0]
            resume_path = self.resumes.get(app_id)
            if resume_path:
                with open(resume_path, 'r') as file:
                    content = file.read()
                job_description = "Describe the job you are applying for here."  # This should be fetched from user input
                cover_letter = generate_cover_letter(content, job_description, api_key='YOUR_OPENAI_API_KEY')
                messagebox.showinfo("Generated Cover Letter", cover_letter)
            else:
                messagebox.showerror("Error", "No resume uploaded for this application.")
        else:
            messagebox.showerror("Error", "Please select an application to generate a cover letter.")
