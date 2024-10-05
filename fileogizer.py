import os
import shutil
from tkinter import *
from threading import Thread
from tkinter import messagebox, filedialog

file_types = {
    'Documents': ('.pdf', '.doc', '.xls', '.txt', '.csv', '.xml', '.zip', '.docx', '.DOCX', '.odt'),
    'Pictures': ('.jpg', '.jpeg', '.png', '.JPG', '.webp'),
    'Videos': ('.mp4', '.mkv', '.3gp', '.flv', '.mpeg'),
    'Music': ('.mp3', '.wav', '.m4a', '.webm'),
    'Programs': ('.py', '.cpp', '.c', '.sh', '.js'),
    'Apps': ('.exe', '.apk'),
}

class File_Organizer:
    def __init__(self, root):
        # Setting the Tkinter main window
        self.window = root
        self.window.geometry("720x500")
        self.window.title('Fileogizer')
        self.window.resizable(width=False, height=False)
        self.window.configure(bg='gray90')
        self.selected_dir = ''
        self.browsed = False

        # Frame 1: For the Logo
        self.frame_1 = Frame(self.window, bg='gray90', width=280, height=70)
        self.frame_1.pack()
        self.frame_1.place(x=20, y=20)

        # About Button
        About_Btn = Button(self.window, text="About",
                           font=("Kokila", 10, 'bold'), bg="dodger blue",
                           fg="white", width=5, command=self.about_window)
        About_Btn.place(x=600, y=20)

        # Exit Button
        Exit_Btn = Button(self.window, text="Exit",
                          font=("Kokila", 10, 'bold'), bg="dodger blue",
                          fg="white", width=5, command=self.exit_window)
        Exit_Btn.place(x=600, y=60)

        # Frame 2: For the Main Page Widgets
        self.frame_2 = Frame(self.window, bg="white", width=720, height=480)
        self.frame_2.place(x=0, y=110)
        self.main_window()

    def main_window(self):
        Heading_Label = Label(self.frame_2,
                              text="Please Select the Folder",
                              font=("Kokila", 20, 'bold'), bg='white')
        Heading_Label.place(x=160, y=20)

        Folder_Button = Button(self.frame_2, text="Select Folder",
                               font=("Kokila", 10, 'bold'), bg="gold", width=10,
                               command=self.select_directory)
        Folder_Button.place(x=130, y=80)

        self.Folder_Entry = Entry(self.frame_2,
                                   font=("Helvetica", 12), width=32)
        self.Folder_Entry.place(x=256, y=85)

        Status = Label(self.frame_2, text="Status: ",
                       font=("Kokila", 12, 'bold'), bg='white')
        Status.place(x=180, y=130)

        # Status Label
        self.Status_Label = Label(self.frame_2, text="Not Started Yet",
                                  font=("Kokila", 12), bg="white", fg="red")
        self.Status_Label.place(x=256, y=130)

        Start_Button = Button(self.frame_2, text="Start",
                              font=("Kokila", 13, 'bold'), bg="dodger blue", fg="white",
                              width=8, command=self._threading)
        Start_Button.place(x=280, y=180)

    def select_directory(self):
        self.selected_dir = filedialog.askdirectory(title="Select a location")
        self.Folder_Entry.delete(0, END)  # Clear entry field before inserting
        self.Folder_Entry.insert(0, self.selected_dir)
        self.browsed = os.path.exists(self.selected_dir)

    def _threading(self):
        self.x = Thread(target=self.organizer, daemon=True)
        self.x.start()

    def organizer(self):
        if not self.browsed:
            messagebox.showwarning('No folders are chosen', 
                                    'Please Select a Folder First')
            return
        try:
            self.Status_Label.config(text='Processing...')
            self.Current_Path = self.selected_dir

            if os.path.exists(self.Current_Path):
                self.Folder_List1 = []
                self.Folder_List2 = []
                self.flag = False

                for folder, extensions in file_types.items():
                    self.folder_name = folder
                    self.folder_path = os.path.join(self.Current_Path, self.folder_name)

                    if os.path.exists(self.folder_path):
                        self.Folder_List1.append(self.folder_name)
                    else:
                        self.Folder_List2.append(self.folder_name)
                        os.mkdir(self.folder_path)

                    for item in self.file_finder(self.Current_Path, extensions):
                        self.Old_File_Path = os.path.join(self.Current_Path, item)
                        self.New_File_Path = os.path.join(self.folder_path, item)
                        shutil.move(self.Old_File_Path, self.New_File_Path)
                        self.flag = True
            else:
                messagebox.showerror('Error!', 'Please Enter a Valid Path!')

            if self.flag:
                self.Status_Label.config(text='Done!')
                messagebox.showinfo('Done!', 'Operation Successful!')
                self.reset()
            else:
                self.Status_Label.config(text='Complete!')
                messagebox.showinfo('Done!', 'Folders have been created. No Files were there to move.')
                self.reset()
        except Exception as es:
            messagebox.showerror("Error!", f"Error due to {str(es)}")

    def file_finder(self, folder_path, file_extensions):
        files = []
        for file in os.listdir(folder_path):
            if any(file.endswith(extension) for extension in file_extensions):
                files.append(file)
        return files

    def reset(self):
        self.Status_Label.config(text='Not Started Yet')
        self.Folder_Entry.delete(0, END)
        self.selected_dir = ''
        self.browsed = False  # Reset the browsed flag

    def about_window(self):
        messagebox.showinfo("Fileogizer", "Developed by Neon-Gr33n")

    def exit_window(self):
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = File_Organizer(root)
    root.mainloop()
