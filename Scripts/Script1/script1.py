'''
Created on 17.09.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

"""
References:
http://pandas.pydata.org/pandas-docs/dev/merging.html
http://pandas.pydata.org/pandas-docs/dev/generated/pandas.io.parsers.read_csv.html
http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.to_csv.html
http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.to_excel.html
http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.sort.html
"""

from os import path, listdir
from pandas import ExcelWriter, read_csv, concat

#Directory containing .csv files that will be concatenated
DataDirState = "InputFiles/_AEIS_State"
DataDirDistrict = "InputFiles/AEIS_District"

class AddStateRow:
    def __init__(self):
        self.ReadData()
        #self.SortData()
        #self.WriteData()
    #end __init__
    
    def ReadData(self):
        print ("\nRead Data")
        if not path.exists(DataDirDistrict):
            print ("\t Data Directory District Does Not Exist")
            exit()
            
        if not path.exists(DataDirState):
            print ("\t Data Directory State Does Not Exist")
            exit()
            
        else:
            """Pandas.concat method takes a list of the DataFrame objects as the parameter.
            That is the reason for creating data_frames list. For every .csv file that is read from
            the DataDir folder, DataFrame object is created by using method read_csv, and those
            objects are appended to the data_frames list. After reading all the files, concat method
            is called with the parameter data_frames list.
            Return value of the concat method is the new concatenated DataFrame"""
            
            data_frames = list()
            #List directory containing the .csv files
            for district_item in listdir(DataDirDistrict):
                #Check the extension of the files, so only .csv files will be considered
                if path.splitext(district_item)[1] == ".csv":
                    f = path.join(DataDirDistrict,district_item)
                    #ovde bih trebao provjeriti fajlove cija imena se poklapaju
                    full_file_name_district = path.splitext(district_item)[0]
                    
                    for state_item in listdir(DataDirState):
                        #Check the extension of the files, so only .csv files will be considered
                        if path.splitext(state_item)[1] == ".csv":
                            f = path.join(DataDirState,state_item)
                            #get full name of the state file
                            full_file_name_state = path.splitext(state_item)[0]
                            
                            if full_file_name_district[:5] == full_file_name_state[:5] :
                                if full_file_name_district[14:] == full_file_name_state[11:] :
                                    print(full_file_name_district)
                                    print(full_file_name_state)
                    
                    #Pandas.read_csv method returns DataFrame object, so we append that object to the data_frames list
                    #data_frames.append(read_csv(f, usecols=Columns, delimiter=",", header=0))
            #self.data = concat(data_frames)  
    #end ReadData

def main():
    AddStateRow()
    print("Finished")
    
if __name__ == "__main__":
    main()