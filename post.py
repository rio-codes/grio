import datetime
time = str(datetime.datetime.now())
print(time)
content=
with open('grioblog.txt', 'a') as file:
    file.write(time +' || '+ content +'\n')




