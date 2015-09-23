'''
Created on 19.09.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat

# Columns that will be extracted from the files
Columns = ["A0CT*YY*R",
           "A0CC*YY*R",
           "A0CSA*YY*R",
           "A0CAA*YY*R",
           "B0CT*YY*R",
           "B0CC*YY*R",
           "B0CSA*YY*R",
           "B0CAA*YY*R",
           "H0CT*YY*R",
           "H0CC*YY*R",
           "H0CSA*YY*R",
           "H0CAA*YY*R",
           "W0CT*YY*R",
           "W0CC*YY*R",
           "W0CSA*YY*R",
           "W0CAA*YY*R",
           "F0CT*YY*R",
           "F0CC*YY*R",
           "F0CSA*YY*R",
           "F0CAA*YY*R",
           "M0CT*YY*R",
           "M0CC*YY*R",
           "M0CSA*YY*R",
           "M0CAA*YY*R",
           "E0CT*YY*R",
           "E0CC*YY*R",
           "E0CSA*YY*R",
           "E0CAA*YY*R"
           ]

DS = {'district': 'D',
      'campus': 'C'}


class SatAct:
    data_dir_input = "AEIS_Campus"
    data_dir_output = "SatActOutputFiles"

    def __init__(self):
        self.CleanOutput()
        self.ReadData()
        self.Merge()
    # end __init__
    
    def Merge(self):
        KeyColumns = self.adjusted
        InputDir = "SatActOutputFiles"

        print("Start merging")

        #Read Inputs
        data_frames = list()
        for item in listdir(InputDir):
            if path.splitext(item)[1] == ".csv":
                f = path.join(InputDir,item)
                data_frames.append(read_csv(f, delimiter=",", header=0, low_memory=False)) 

        #Merge data
        data = data_frames[0]

        for item in data_frames[1:]:
            data = data.append(item)

        #Write output
        data.to_csv(InputDir + "\\" + self.dis_cam + "_SatAct.csv", sep=",", index = False)

        print ("Finished merge")
    # end Merge

    def AdjustColumn(self, ds, year=None):
        adjusted_columns = list()
        # add district/campus and year to columns
        if ds == 'district':
            adjusted_columns.append('DISTRICT')
        elif ds == 'campus':
            adjusted_columns.append('CAMPUS')
        adjusted_columns.append('YEAR')

        for column in Columns:
            if ds is not None:
                column = DS[ds] + column
            if year is not None:
                column = column.replace('*YY*', year)
            adjusted_columns.append(column)
        return adjusted_columns
    # end AdjustColumns

    def CleanOutput(self):
        if exists(self.data_dir_output):
            for item in listdir(self.data_dir_output):
                remove(join(self.data_dir_output, item))
    # end CleanOutput

    def ReadData(self):
        print("\nRead Data")
        if not path.exists(self.data_dir_input):
            print("\t Data Directory Does Not Exist")
            exit()
        else:

            # List directory containing the .csv files
            for item in listdir(self.data_dir_input):
                # Check the extension of the files,
                # so only .csv files will be considered
                name_of_file = path.splitext(item)[0]
                name_parts = name_of_file.split("_")
                name_year = str(int(name_parts[0]) - 1)
                ds = name_parts[1]
                self.dis_cam = ds

#                 for column in DistrictColumns:
#                     if column != "DISTRICT" and column != "YEAR":
#                         if column[5:6].isdigit():
#                             column_new = column[:5] + name_year[2:4] + column[7:8]
#                         else:
#                             column_new = column[:6] + name_year[2:4] + column[8:9]
# 
#                         loc = DistrictColumns.index(column)
#                         DistrictColumns.remove(column)
#                         DistrictColumns.insert(loc, column_new)
        

                if path.splitext(item)[1] == ".csv" and name_parts[2] == "college":
                    file_path = path.join(self.data_dir_input, item)
                    adjusted_columns = self.AdjustColumn(ds=ds, year=name_year[2:4])
                    self.adjusted = adjusted_columns

                    # Pandas.read_csv method returns DataFrame object
                    try:
                        data_frame = read_csv(file_path,
                                          usecols=adjusted_columns,
                                          delimiter=",",
                                          header=0)
                        self.WriteData(data_frame, item)
                    except:
                        print("Error while reading %s" % item)
                        print("Columns: %s\n" % adjusted_columns)

    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(self.data_dir_output):
            mkdir(self.data_dir_output)
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.data_dir_output, output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    SatAct()
    print("Finished")

if __name__ == "__main__":
    main()
