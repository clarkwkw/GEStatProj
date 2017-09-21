import tkinter as tk
import json

left_padding = 20

def ask_input(title, dtype = str, default_val = None):
	result = ""
	while True:
		try:
			if default_val is not None:
				result = input("%s [%s]: "%(title, default_val))
			else:
				result = input("%s: "%title)

			if len(result.strip()) != 0:
				result = dtype(result.strip())
				break

			elif default_val is not None:
				return default_val
		except ValueError:
			pass
		print("invalid value, try again")

	return result

class EntryWindow:
	def __init__(self, text_type, batch_name, start_batch_no, batch_no_width):
		self.text_type = text_type
		self.batch_name = batch_name
		self.batch_no = start_batch_no
		self.batch_no_width = batch_no_width

		self.window = tk.Tk()
		self.window.title("Convert texts")
		self.window.geometry('700x450')
		self.title = tk.Label(self.window, text = self.__get_cur_file_name())
		self.title.place(x = left_padding, y = 10)

		self.question = self.__create_input_line("Question", y = 40)
		self.think = self.__create_input_line("HL thinking score", y = 70, input_type = "double")
		self.understand = self.__create_input_line("Understanding score", y = 100, input_type = "double")
		self.lang = self.__create_input_line("Language score", y = 130, input_type = "double")
		self.pres = self.__create_input_line("Presentation score", y = 160, input_type = "double")
		self.text = self.__create_input_area("Text", y = 190)
		self.comment = self.__create_input_area("Comment", y = 280)

		self.error_msg = tk.Label(self.window, text = "", fg = "red")
		self.error_msg.place(x = left_padding, y = 380)

		self.submit_button = tk.Button(self.window, text = "Create", command = self.save_text)
		self.submit_button.place(x = 180, y = 400)

		self.skip_button = tk.Button(self.window, text = "Skip", command = self.__increase_batch_no)
		self.skip_button.place(x = 360, y = 400)
		self.window.mainloop()

	def save_text(self):
		batch_no_str = "{batch_no:0{width}}".format(batch_no = self.batch_no, width = self.batch_no_width)
		try:
			question = self.question.get().strip()
			text = self.text.get("1.0",tk.END).strip()
			if len(question) == 0:
				self.error_msg.config(text = "Error: Question cannot be empty")
				return 

			if len(text) == 0:
				self.error_msg.config(text = "Error: Text cannot be empty")
				return

			json_dict = {
				"type": self.text_type,
				"batch_name": self.batch_name,
				"batch_no": batch_no_str,
				"question": question,
				"score": {
					"think": self.think.get(),
					"understand": self.understand.get(),
					"lang": self.lang.get(),
					"pres": self.pres.get()
				},
				"text": text
			}

		except tk.TclError:
			self.error_msg.config(text = "Error: wrong score, must be a decimal")
			return

		comment = self.comment.get("1.0", tk.END).strip()
		if len(comment) > 0:
			json_dict["comment"] = comment

		with open(self.__get_cur_file_name(), "w") as f:
			json.dump(json_dict, f, indent = 4)

		
		self.error_msg.config(text = "")
		self.__increase_batch_no()

	def __increase_batch_no(self):
		self.batch_no += 1
		self.title.config(text = self.__get_cur_file_name())
		self.question.set("")
		self.think.set(0)
		self.understand.set(0)
		self.lang.set(0)
		self.pres.set(0)
		self.text.delete(1.0, tk.END)
		self.comment.delete(1.0, tk.END)

	def __get_cur_file_name(self):
		batch_no_str = "{batch_no:0{width}}".format(batch_no = self.batch_no, width = self.batch_no_width)
		file_name = "%s-%s-%s.json"%(self.text_type, self.batch_name, batch_no_str)
		return file_name
	
	def __create_input_line(self, title, y, input_type = "string", default_val = None):
		tk.Label(self.window, text = "%s: "%title).place(x = left_padding, y = y)
		if input_type == "string":
			tk_input_var = tk.StringVar()
		elif input_type == "double":
			tk_input_var = tk.DoubleVar()
		else:
			raise Exception("unexpected input type '%s'"%(input_type))
		if default_val is not None:
			tk_input_var.set(default_val)
		tk_input_entry = tk.Entry(self.window, textvariable = tk_input_var)
		tk_input_entry.place(x = 200 + left_padding, y = y)

		return tk_input_var

	def __create_input_area(self, title, y):
		tk.Label(self.window, text = "%s: "%title).place(x = left_padding, y = y)

		text_area = tk.Text(self.window, height = 5, width = 50, borderwidth = 2)
		text_area.place(x = 200 + left_padding, y = y)

		return text_area

if __name__ == "__main__":
	text_type = ask_input("Text type", default_val = "TP")
	batch_name = ask_input("Batch name")
	start_batch_no = ask_input("Starting batch no.", dtype = int)
	batch_no_width = ask_input("Batch no. width", dtype = int)
	EntryWindow(text_type, batch_name, start_batch_no, batch_no_width)