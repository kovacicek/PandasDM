'''
Created on 26.10.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat, merge, pivot, pivot_table
from pandas.core.frame import DataFrame

# Columns that will be extracted from the files
Columns = ["CAMPUS",
           "YEAR",
           "REGION",
           "DISTRICT",
           "DNAME",
           "CNAME",
           "Subject",
           "Grade",
           "Language",
           "Category",
           "all"
           ]

ColumnsEXIT = ["CAMPUS",
           "YEAR",
           "REGION",
           "DISTRICT",
           "DNAME",
           "CNAME",
           "Subject",
           "Grade",
           "Language",
           ]

values = [
          "rs",
          "d",
          "satis_rec_nm",
          "satis_ph1_nm"
          ]

class StaarPivot:
    script_name = "StaarPivot"
    data_frames = list()

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.CleanOutput()
        self.Process()
    # end __init__

    def CleanOutput(self):
        """
        Cleans output dir if exists
        """
        print("Clean Output")
        if exists(self.output_dir):
            for item in listdir(self.output_dir):
                remove(join(self.output_dir, item))
            print("\t output dir cleaned: %s" % (self.output_dir))
    # end CleanOutput

    def Process(self):
        print("\nRead Data")
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):

            name_of_file = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                print("File path: " + file_path)
                # Pandas.read_csv method returns DataFrame object
                # processing starts from here
                # 21901001,15,6,21901,college station, A&M Cons HS, a1, EOC, English, 284, 4006, 243, 150

                # try:
                data_frame = read_csv(file_path,
                                      usecols=Columns,
                                      delimiter=",",
                                      header=0,
                                      nrows=12960,
                                      low_memory=False)
                print (data_frame.columns[:-2])
                data_frame = data_frame.pivot(index="CAMPUS",
                                              columns="Category",
                                              values="all")
                print(data_frame)
                self.WriteData(data_frame, "test.csv")
               # except:
                   # print("Error while reading %s" % filename)
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.output_dir, output_name),
                          sep=",",
                          index=True)
    # end WriteData


def main():
    staar_merged = "4_staar_merged"
    staar_pivot = "5_staar_pivot"

    for item_dir in listdir(staar_merged):
        input_dir = join(staar_merged, item_dir)
        output_dir = join(staar_pivot, item_dir)   
        StaarPivot(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
    