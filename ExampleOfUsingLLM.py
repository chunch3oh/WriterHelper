import FunctionOfSQLite as fsql

NameOfDB = 'Books'
WorkingChapter = 'CH1'
NewAddChpter = 'CH2'
NewContent = 'ch1_new'
Column = ['Title', 'Introduction', 'Characters', 'CH1']
Content = ['Azkaban', 'Story', 'Voldemore', 'ch1_old']

fsql.Building(NameOfDB, Column, Content)
fsql.AddColumn(NameOfDB, NewAddChpter, "CH2_old")
content = fsql.TakeContent(NameOfDB, WorkingChapter)
print(content)
fsql.Update(NameOfDB, WorkingChapter, NewContent)
content = fsql.TakeContent(NameOfDB, WorkingChapter)
print(content)
fsql.drop()
