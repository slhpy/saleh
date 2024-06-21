from balebot import Bot
import random
import time
for i in range(1,100000000000):
    try :
        c = ['d','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']

        a= random.choice(c)
        b= random.choice(c)
        ee= random.choice(c)
        d= random.choice(c)
        e= random.choice(c)
        f= random.choice(c)
        g= random.choice(c)
        h= random.choice(c)
        r= random.choice(c)
        pp= random.choice(c)
        gg= random.choice(c)        
        qq = f"{a}{b}{ee}{d}{e}{f}{i}{pp}{gg}{r}{h}{g}" 
        bot = Bot(qq, True)
        with open('france.txt', 'r') as f:
            lines = f.readlines()
            
#
#        # انتخاب رندوم یک خط
        from balecode import random_line
        lines.remove(random_line)

        with open('france.txt', 'w') as f:
            # نوشتن خطوط باقی‌مانده در فایل
            for line in lines:
                f.write(line)

        print('------------------- \n')
    except:
        print('error')
        print('------------------- \n')