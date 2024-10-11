


class BMPModelOffline:
    def __init__ (self, Vrxn, Vf, tp):
        self.Vrxn = Vrxn
        self.Vf = Vf
        self.tp = tp

    def MixtureCalculation (self, substratesNumber, MixtureRule,
                            Fraction1, Volume1, Weight1, TS1, VS1, rho1, Cc1, Hc1, Oc1, Nc1, Sc1,
                            Fraction2, Volume2, Weight2, TS2, VS2, rho2, Cc2, Hc2, Oc2, Nc2, Sc2,
                            Fraction3, Volume3, Weight3, TS3, VS3, rho3, Cc3, Hc3, Oc3, Nc3, Sc3,
                            Fraction4, Volume4, Weight4, TS4, VS4, rho4, Cc4, Hc4, Oc4, Nc4, Sc4):
        if substratesNumber == 1 and MixtureRule == "Fracción":
            pass

