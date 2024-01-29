class CheeseMeasure():
    
    def __init__(self, dataframe) -> None:
        self.dataframe = dataframe
        
    def countby_families(self, ax):
        
        columns = ['families', 'cheeses']
        grb_by_families = self.dataframe[columns].groupby('families').count()
        grb_by_families['percent'] = grb_by_families['cheeses'] / grb_by_families['cheeses'].sum()
        grb_by_families['percent'] = grb_by_families['percent'].round(4)*100

        mask = grb_by_families['percent'] <= 5
        grb_by_families['custom_group'] = grb_by_families.index
        grb_by_families['custom_group'].loc[mask] = 'Autres'

        columns = ['custom_group', 'percent']
        grb_by_families = grb_by_families[columns].groupby('custom_group').sum()

        grb_by_families.plot(kind="pie", y="percent", autopct='%1.2f%%', legend=False, ylabel='', shadow=True, title="Répartition du nombre de fromage par famille", ax=ax)

        return grb_by_families