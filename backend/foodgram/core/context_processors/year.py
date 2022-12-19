""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+
 
file year.py -> печать текущего года 
""" 
from datetime import datetime

def year(request):
    dt = datetime.now().year
    return {
       'year': dt
    }
