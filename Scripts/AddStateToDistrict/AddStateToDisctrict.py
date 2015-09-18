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

from os import listdir
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat


class AddStateRow:
    # Directory containing .csv files that will be concatenated
    data_dir_state = "InputFiles/_AEIS_State"
    data_dir_district = "InputFiles/AEIS_District"

    def __init__(self):
        self.ReadData()
        #self.SortData()
        #self.WriteData()
    #end __init__

    def ReadData(self):
        print ("\nRead Data")
        if not exists(self.data_dir_district):
            print ("\t Data Directory District Does Not Exist")
            exit()

        elif not exists(self.data_dir_state):
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
            # List directory containing the .csv files
            for district_item in listdir(self.data_dir_district):
                # Check only .csv files
                if splitext(district_item)[1] == ".csv":
                    district_file_path = join(self.data_dir_district,
                                              district_item)
                    # ovde bih trebao provjeriti fajlove cija imena se poklapaju
                    full_file_name_district = splitext(district_item)[0]

                    # Find proper state file
                    self.FindProperStateFile(full_file_name_district)
                    
                    #Pandas.read_csv method returns DataFrame object, so we append that object to the data_frames list
                    #data_frames.append(read_csv(f, usecols=Columns, delimiter=",", header=0))
            #self.data = concat(data_frames)  
    #end ReadData
    def FindProperStateFile(self, district_filename):
        """
        It returns file
        """
        for state_item in listdir(self.data_dir_state):
            # Check only .csv files
            if splitext(state_item)[1] == ".csv":
                state_file_path = join(self.data_dir_state, state_item)
                #get full name of the state file
                state_filename = splitext(state_item)[0]
                tmp = state_filename.replace("state", "district")
                if district_filename == tmp:
                    print(district_filename, state_filename)
                    return state_file_path
        else:
            print("There is no corresponding file for %s" % district_filename)

#                 if full_file_name_district[:5] == full_file_name_state[:5]:
#                     if full_file_name_district[14:] == full_file_name_state[11:]:
#                         print(full_file_name_district)
#                         print(full_file_name_state)

def main():
    AddStateRow()
    print("Finished")
    
if __name__ == "__main__":
    main()