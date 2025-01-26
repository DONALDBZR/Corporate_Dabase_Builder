from sys import path


path.insert(0, "/home/darkness4869/Documents/Corporate_Database_Builder")


from Models.Builder import Builder


Corporate_Database_Builder = Builder()
Corporate_Database_Builder.curateMembers()
