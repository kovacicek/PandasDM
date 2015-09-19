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
Columns = [
           "DA0CT13R",
           "DA0CC13R",
           "DA0CSA13R",
           "DA0CAA13R",
           "DB0CT13R",
           "DB0CC13R",
           "DB0CSA13R",
           "DB0CAA13R",
           "DH0CT13R",
           "DH0CC13R",
           "DH0CSA13R",
           "DH0CAA13R",
           "DW0CT13R",
           "DW0CC13R",
           "DW0CSA13R",
           "DW0CAA13R",
           "DF0CT13R",
           "DF0CC13R",
           "DF0CSA13R",
           "DF0CAA13R",
           "DM0CT13R",
           "DM0CC13R",
           "DM0CSA13R",
           "DM0CAA13R",
           "DE0CT13R",
           "DE0CC13R",
           "DE0CSA13R",
           "DE0CAA13R"
           ]


class SatAct:
    data_dir_input = "..\AddStateToDistrict\OutputFiles"
    data_dir_output = "SatActOutputFiles"

    def __init__(self):
        self.CleanOutput()
        self.ReadData()
    # end __init__

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

                if path.splitext(item)[1] == ".csv" and name_parts[2] == "college":
                    file_path = path.join(self.data_dir_input, item)

                    # Pandas.read_csv method returns DataFrame object
                    try:
                        data_frame = read_csv(file_path,
                                          usecols=Columns,
                                          delimiter=",",
                                          header=0)
                        self.WriteData(data_frame, item)
                    except:
                        pass
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
