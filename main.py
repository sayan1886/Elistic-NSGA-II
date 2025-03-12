
from nsga2.example.config import config

from nsga2.example import kur, sch, zdt1

if __name__ == "__main__":
    lang='KUR'
    match lang:
        case "KUR":
            kurConfig = config.get_config("kur")
            kur.kur(kurConfig)
        case "SCH":
            schConfig = config.get_config("sch")
            sch.sch(schConfig)
        case "ZDT1":
            zdtOneConfig = config.get_config("zdt1")
            zdt1.zdt1(zdtOneConfig)
        case "ZDT4":
            print("no option")
