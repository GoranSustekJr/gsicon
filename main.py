from ves import Veslac

l = []

print(len(str(12345678901)))

with open('PodaciVeslaca.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        try:
            ime, oib, grod, vr = line.strip().split(', ')
            a = Veslac(oib, ime, grod, float(vr))
            l.append(a)
        except Exception as e:
            print(e)

with open('PodaciVremena.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        for i in range(len(l)):
            try:
                if l[i][1] == line[0]:
                    l[i].promijenivrijeme(float(line[1]))
                    
            except Exception as e:
                print(e)
                
i = input()
ime, oib, grod, vr = i.strip().split(', ')

file = open('PodaciVeslaca.txt', 'a')
file.write(f"\n{ime}, {oib}, {grod}, {float(vr)}")