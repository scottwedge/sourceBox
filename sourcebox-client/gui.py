# -*- coding: utf-8 -*-#
#
# sourceboxclient – gui
#
# @encode  UTF-8, tabwidth = 4 , newline = LF
# @date   14.06.13
# @author  Johannes
#

import Tkinter, tkFileDialog, tkMessageBox, Tkconstants



class gui:
	def __init__(self):
		self.root = Tkinter.Tk()
		self.root.title("SourceBox")
		 
		self.statusLabel = Tkinter.Label(self.root)
		self.statusLabel.pack()
		
		self.statusButton = Tkinter.Button(self.root, command = self.changeStatus)
		self.statusButton.pack()
		
		Tkinter.Button(self.root, text = "Optionen", command = self.optionWindow).pack()
		
		self.aktStatus = 'sleep'
		self.displayStatus()
		
		Tkinter.Label(self.root, text = "Folgende Dateien wurden für andere Benutzer gesperrt:").pack()
		lockedLabel = Tkinter.Label(self.root)
		
		Tkinter.Button(self.root, text = "Teste Meldungen", command = self.testError).pack()
		
		self.root.mainloop()
		
	def infoBox(self, title, text):
		tkMessageBox.showinfo(title, text)
		
	def errorBox(self, title, text):
		tkMessageBox.showerror(title, text)
		
	def warningBox(self, title, text):
		tkMessageBox.showwarning(title, text)
	
	def testError(self):
		self.errorBox('TEST', 'Das ist ein Test der Fehlermeldung.')
		self.infoBox('TEST', 'Das ist ein Info-Test.')
		self.warningBox('TEST', 'Das ist ein Test der Warnungsmeldung.')
	
	def displayStatusText(self, text, button):
		self.statusLabel.config(text = text)
		self.statusButton.config(text = button)
	
	def displayStatus(self):
		if self.aktStatus == 'active':
			self.displayStatusText('SourceBox ist aktiv.', 'Anhalten')
		else:
			self.displayStatusText('SourceBox ist nicht aktiv.', 'Starten')
	
	def changeStatus(self):
		if self.aktStatus == 'sleep':
			self.aktStatus = 'active'
		else:
			self.aktStatus = 'sleep'
		self.displayStatus()
	
	def optionWindow(self):
		self.oWin = Tkinter.Toplevel()
		self.oWin.title("Optionen")
		
		Tkinter.Label(self.oWin, text="Server IP-Adresse").grid(row=0)
		self.eServerIP = Tkinter.Entry(self.oWin)
		self.eServerIP.grid(row=0, column=1)
		#self.eServerIP.insert(0,...)
		
		Tkinter.Label(self.oWin, text="Ordner").grid(row=1)
		self.eDirectory = Tkinter.Entry(self.oWin)
		#self.eDirectory.insert(0,...)
		self.eDirectory.grid(row=1, column=1)
		Tkinter.Button(self.oWin, text = "Ordner auswählen", command = self.askDirectory).grid(row=1, column=2)
		
		Tkinter.Button(self.oWin, text='Übernehmen', command=self.assumeOptions).grid(row=3, column=0, pady=4)
		Tkinter.Button(self.oWin, text='Abbrechen', command=self.cancelOptions).grid(row=3, column=1, pady=4)
	
	def askDirectory(self):
		self.eDirectory.delete(0, Tkinter.END)
		self.eDirectory.insert(0, tkFileDialog.askdirectory(initialdir=self.eDirectory.get()))
	
	def assumeOptions(self):
		pass
	
	def cancelOptions(self):
		self.oWin.destroy()


#testing
mygui = gui()