from datetime import datetime,timedelta
import time

class Maksukortti:
    """Maksukorttiluokka jossa on vain yksi field 'saldo'"""
    def __init__(self, saldo):
        self.saldo = saldo
        self.lippu = None

    def lataaRahaa(self, summa):
        """Lataa rahaa kortille"""
        self.saldo += summa

    def maksa(self, summa):
        """Ota rahaa kortilta mikäli summa on pienempi kuin kortin saldo"""
        if summa < self.saldo:
            self.saldo -= summa
            print("Maksu onnistui (summa: {summa} €), saldo nyt: {saldo} €)".format(summa=summa,saldo=self.saldo))
            return True
        print("Maksu epäonnistui (summa: {summa} €), kortilla ei tarpeeksi saldoa (saldo: {saldo} €)".format(summa=summa,saldo=self.saldo))
        return False
    
    def annaSaldo(self):
        print("Kortin saldo on {saldo} €".format(saldo=self.saldo))

    def tarkistaLippu(self, zone):
        """Lippu on voimassa jos lipun zone on vähemmän kuin tarkistus-zone ja aika on enemmän kuin 2 tuntia menneisyydessä"""
        if self.lippu:
            self.lippu.tarkista_lippu(zone)
        return False
    
    def lataaLippu(self, zone):
        self.lippu = Lippu(zone)

class LippuAutomaatti:
    """Lippuautomaatti josta voidaan ostaa lippuja"""
    def __init__(self, nimi):
        self.nimi = nimi
    
    def ostaLippu(self, zone, maksukortti):
        """Vyöhykkeitä (zone) on 3 erilaista, zone-parametri pitää olla kokonaisluku 1-3"""
        if zone == 1:
            hinta = 2.06
        elif zone == 2:
            hinta = 4.04
        elif zone == 3:
            hinta = 6.09
        else:
            print("Vyöhykkeen valinta epäonnistui. Valitse vyöhyke kokonaisluvulla 1-3")
            return False
        
        if not maksukortti.tarkistaLippu(zone):
            if maksukortti.maksa(hinta):
                maksukortti.lataaLippu(zone)
                return True
        else:
            print("Lipun osto vyöhykkeelle {zone} epäonnistui. Kortillasi on jo voimassaoleva lippu vyöhykkeelle: {korttiZone}".format(
                zone=zone,
                korttiZone=maksukortti.lippu.zone)
            )
            return False

        return False
        
class Lippu:
    def __init__(self, zone):
        hours = 2 # ticket is valid two hours from purchase time
        timeNow = datetime.now()
        checkTime = timeNow + timedelta(hours = hours)

        self.zone = zone
        self.buyTime = timeNow
        self.checkTime = checkTime
    
    def tarkista_lippu(self, zone):
        timeNow = datetime.now()
        timeDiff = self.checkTime - timeNow
        diffInMinutes =  round(timeDiff.total_seconds() / 60, 1)

        if self.zone >= zone and self.checkTime > timeNow:
            print("Lippu on voimassa ({minutes} min). Tarkistusvyöhyke: {zone}".format(zone=zone,minutes=diffInMinutes))
            return True
        
        print("Lippu ei ole voimassa. Tarkistusvyöhyke: {zone}".format(zone=zone))
        return False

class Hinnat:
    luettelo = (
        2.90, # zone 1
        3.50, # zone 2
        4.50  # zone 3
    )

    @staticmethod
    def anna_hinta(zone):
        if zone in range(0,len(Hinnat.luettelo)):
            return Hinnat.luettelo[zone]
        return False

def main():
    
    lippuAutomaatti = LippuAutomaatti("VR123")
    maksukortti = Maksukortti(0)

    maksukortti.lataaRahaa(3.00)
    lippuAutomaatti.ostaLippu(1, maksukortti)

    maksukortti.tarkistaLippu(1)


main()