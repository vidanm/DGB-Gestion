from .charges import *
import pandas as pd
import datetime as dt

class Synthese():
    
    def __init__(self,charges):

        self.col = ['CHANTIER','BUDGET','DEP DU MOIS','DEP CUMULEES','PFDC','MARGE THEORIQUE (€)','MARGE THEORIQUE (%)','MARGE BRUTE (€)','MARGE BRUTE (%)']

        self.charges = charges
        self.synthese_annee = pd.DataFrame(None,None,columns=self.col)
        self.synthese_cumul = self.synthese_annee.copy(deep=True)
    
    def ajoute_synthese_annee(self,data):
        self.synthese_annee = self.synthese_annee.append(data,ignore_index=True)

    def calcul_synthese_annee(self,mois,annee):
        chantier_names = self.charges.get_chantier_names()
        for name in chantier_names:
            
            if 'DIV' in name or 'STRUCT' in name:
                continue

            chantier_line = ["",0,0,0,0,0,0,0,0]
            chantier_line[0] = name

            for index,row in self.charges.get_raw_chantier(name).iterrows():
                date = row['Date']
                if (row['Journal'] == 'ACH') and (date.month <= mois) and (date.year == annee):
                    chantier_line[3] += row['Débit'] - row['Crédit']
                    if (date.month == mois):
                        chantier_line[2] += row['Débit'] - row['Crédit']
            
            out = pd.DataFrame([chantier_line],columns=self.col)
            self.ajoute_synthese_annee(out)
