import FunctionOfSQLite as fsql

NameOfDB = 'Books'
WorkingChapter = 'CH1'
NewAddChpter = 'CH2'
NewContent = 'ch1_new'
Column = ['Title', 'Introduction', 'Characters', 'CH1']
Content = ['Azkaban', 'Story', 'Voldemore', 'ch1_old']

fsql.create_table(NameOfDB, Column)
fsql.insert_values(NameOfDB, Column, Content)
fsql.add_column(NameOfDB, NewAddChpter, "CH2_old")
content = fsql.get_content(NameOfDB, WorkingChapter)
print(content)
fsql.update(NameOfDB, WorkingChapter, NewContent)
content = fsql.get_content(NameOfDB, WorkingChapter)
print(content)
fsql.drop()
