

from app.execute._app import Application
from app.execute._create_dataset import CreateDataset


from app.ui._app import MainApp

input_variables = [
    {
        'source':'MODIS/061/MYD13Q1',
        'variable':'NDVI'

    },
    {
        'source':'MODIS/061/MOD11A1',
        'variable':'LST_Day_1km'

    },
    {
        'source':'NASA/ORNL/DAYMET_V4',
        'variable':'prcp'

    }


    
]
    


#app = Application(input_variables)
#app.execute({'Latitud':20.57,'Longitud':-90.22524},'2022-10-10')
#cd = CreateDataset()
#cd.execute('2022',96,'gee-coordinates-2022/', variables)
#cd.create_ts_file('2023')
#cd.catch22_transform('2022')


  
 
  
  
# Driver Code
app = MainApp()
app.mainloop()