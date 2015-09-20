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
DistrictColumns = ["DISTRICT",
                   "YEAR",
                   "DPERRAKR",
                   "DPERRA1R",
                   "DPERRA2R",
                   "DPERRA3R",
                   "DPERRA4R",
                   "DPERRA5R",
                   "DPERRA6R",
                   "DPERRA7R",
                   "DPERRA8R"
                   ]


class Retention:
    data_dir_input = "..\AddStateToDistrict\OutputFiles"
    data_dir_output = "RetentionOutputFiles"

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

                if path.splitext(item)[1] == ".csv" and name_parts[2] == "student":
                    file_path = path.join(self.data_dir_input, item)

                    # Pandas.read_csv method returns DataFrame object
                    try:
                        data_frame = read_csv(file_path,
                                          usecols=DistrictColumns,
                                          delimiter=",",
                                          header=0)
                        self.WriteData(data_frame, item)
                    except:
                        print("Error while reading %s" % item)
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
    Retention()
    print("Finished")

if __name__ == "__main__":
    main()
