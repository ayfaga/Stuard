import pandas as pd

def run():
    with open("zakaz.txt", 'r', encoding='utf-8') as f:
        a=f.readlines()
    open("zakaz.txt",'w').close()

    for i in a:
        i=i.replace("\n", '')
        try:
            df = pd.read_csv('bdpokyp.csv', encoding="utf-8", sep=";")
        except:
            df = pd.read_csv('bdpokyp.csv', encoding="windows-1251", sep=";")
        i1=i.split(',')[0]
        i1 = i1.split()
        i2=i.split(', ')[3:]
        result = df[
            (df['Фамилия'] == i1[0]) &
            (df['Имя'] == i1[1]) &
            (df['Отчество'] == i1[2])
        ]
        
        # Если запись найдена, возвращаем индекс
        if not result.empty:
            # Если строка найдена, работаем со столбцом "Серия"
            index_to_update = result.index[0]  # Получаем индекс найденной строки
            # Текущее значение в "Серия"
            current_value = df.at[index_to_update, "Что было заказано?"]
            if current_value == '-':
                current_value = i2
                
            else:
                current_value = current_value.split(',')
                current_value1 = []
                i3=[]
                for y in current_value:
                    current_value1.append(y.split()[0])
                for y in i2:
                    i3.append(y.split()[0])
                for x in i3:
                    if x in current_value1:
                        vrem = current_value[current_value1.index(x)]
                        vrem = vrem.split()
                        vrem2 = vrem[-1][1:]
                        if x in i3:
                            vrem3 = i2[i3.index(x)]
                            vrem3 = vrem3.split()
                            vrem4 = vrem3[-1][1:]
                        vrem5 = str(int(vrem2) + int(vrem4))
                        vrem6=current_value[current_value1.index(x)].split('x')
                        current_value[current_value1.index(x)] = ('x'.join([vrem6[0], vrem5]))
                    if x not in current_value1:
                        current_value.append(i2[i3.index(x)])
            current_value = ", ".join(current_value)

            while current_value.replace('  ', ' ') != current_value:
                current_value = current_value.replace('  ', ' ')
            df.at[index_to_update, "Что было заказано?"] = current_value  # Обновляем значение
        df.to_csv("bdpokyp.csv", sep=";", index=False, encoding="windows-1251")

run() 