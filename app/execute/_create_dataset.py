
import pandas as pd
import numpy as np
from aeon.datasets import load_from_tsfile
from aeon.transformations.collection.convolution_based import Rocket
from aeon.transformations.collection.feature_based import Catch22
        
from datetime import timedelta
from datetime import datetime

class CreateDataset:

    def __init__(self) -> None:
        pass


    def get_series(self,folder,variable,row):

        df = pd.read_csv(folder + variable['folder'] +'/' +  str(row['Latitud']) + '_' + str(row['Longitud']) + '.csv')
        if variable['folder'] == 'SOIL' or variable['folder']=='DAYMET_V4':
            df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')  
        else:
            df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')  
    
        df = df.set_index('date').asfreq('D', method='ffill').reset_index()
        
        mask = (df['date'] > row['Fecha_inicio']) & (df['date'] <= row['Fecha'])
        df = df.loc[mask]
        list_f = df[variable['variable']].values.tolist()
        len_list = len(list_f)  
        if len_list == 0:
            return [0]*96
        if len_list != 96:
            print(variable)
            print(len_list)
            for i in range(len_list,96):
                list_f.append(list_f[len_list-1])

        return list_f

    def execute(self,filename,num_days,folder,variables):
        data = pd.read_csv(f"data/{filename}.csv")
        data = data[data['Actividad_Realizada'] == 'Exploración']
        data.drop(data[data['Resultado']=='En proceso'].index, inplace=True)

        data_output = data[['Fecha','Latitud','Longitud','Resultado']]
        data_output.loc[:,'Fecha'] = data_output['Fecha'].astype('datetime64[s]')
        data_output.loc[:,'Fecha_inicio'] = data_output['Fecha'] - timedelta(days=num_days)

        for variable in variables:
            print(variable)
            data_output[variable['variable']] = data_output.apply(lambda row: self.get_series(folder,variable,row), axis=1)

        dataset = data_output[[variable['variable'] for variable in variables]+['Resultado']]
        dataset.to_csv(f"data/{filename}-dataset.csv", index=False) 


    def create_ts_file(self, filename):
        with open(f"data/{filename}-dataset.csv", 'r') as f:
            f.readline()

            

 
 
            s = f.read()
            
            s = s.replace(']","[', ':')
            s = s.replace(']",', ':')
            s = s.replace('"[', '')
            with open(f"data/{filename}-dataset.ts",'w') as f2:
                f2.seek(0)
                f2.write(f"@problemName {filename}-locust\n")
                f2.write("@missing false\n")
                f2.write("@univariate false\n")
                f2.write("@dimension 13\n")
                f2.write("@equallength true\n")
                f2.write("@serieslength 96\n")
                f2.write("@classlabel true Positivo Negativo\n")
                f2.write("\n")
                f2.write("@data\n")

                f2.write(s)



    def rocket_transform(self,filename):
        X,y = load_from_tsfile(f"data/{filename}-dataset.ts")
        rocket = Rocket()
        #catch22 = Catch22()
        X_ = rocket.fit_transform(X)
        df = pd.DataFrame(X_)
        df['Resultado'] = y
        df.to_csv(f"data/{filename}-rocket.csv",index=False)


    def catch22_transform(self,filename):
        X,y = load_from_tsfile(f"data/{filename}-dataset.ts")
        catch22 = Catch22()
        X_ = catch22.fit_transform(X)
        df = pd.DataFrame(X_)
        df['Resultado'] = y
        df.to_csv(f"data/{filename}-catch22.csv",index=False)