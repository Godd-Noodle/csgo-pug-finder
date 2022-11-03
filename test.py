from  faceit import FaceitData
import sqlite3



def main():
    #faceitApi()
    sqlLite()

def faceitApi():
    print("faceitAPI")
    fd = FaceitData("a396ecc3-62e2-4f59-bf07-ef7b47d929b4")
    #fd = FaceitData("1-e40b562d-484e-45e0-b974-3b8921492d66")
    match_details = FaceitData.player_details(fd,"Godd_Noodle","csgo")
    #Godd_Noodle = fd.player_stats("Godd_Noodle", "")
    print(match_details)
    

def sqlLite():
    #test
    print("sqlLite")
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    

if  __name__ == "__main__":
    main()