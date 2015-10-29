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

# Columns related to pivoting
index_col = "CAMPUS"
pivot_col = "Category"
value_col = "ecoy"

# Columns that will be extracted from the files
Columns = [index_col,
           "YEAR",
           "REGION",
           "DISTRICT",
           "DNAME",
           "CNAME",
           "Subject",
           "Grade",
           "Language",
           pivot_col,
           value_col
           ]

Cols = [index_col,
           "YEAR",
           "REGION",
           "DISTRICT",
           "DNAME",
           "CNAME",
           "Subject",
           "Grade",
           "Language",
           pivot_col
           ]


class StaarPivot:
    script_name = "StaarPivot"
    data_frames = list()

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        # self.CleanOutput()
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
        else:
            print("\t output dir does not exist: %s" % (self.output_dir))
    # end CleanOutput

    def Process(self):
        print("\nRead Data")
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):
            name_of_file = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                print("File path: " + file_path)

                try:
                    df = read_csv(file_path,
                                  usecols=Columns,
                                  delimiter=",",
                                  header=0,
                                  low_memory=False)

                    # remove duplicate entries from the df
                    # they will produce ValueError: can't reshape...
                    # if not removed
                    # df.drop_duplicates(subset=[index_col, pivot_col], inplace=True)

                    # create pivot table from df
#                     df_pivot = df.pivot(index=index_col,
#                                         columns=pivot_col,
#                                         values=value_col)

                    df_pivot = df.set_index(Cols).unstack(pivot_col)

#                     # Campus column is considered as an index in the df_pivot
#                     # add it as a column to the frame
#                     df_pivot[index_col] = df_pivot.index
# 
#                     # remove pivot_col and value_col from df
#                     df.drop([pivot_col, value_col], axis=1, inplace=True)
# 
#                     # remove duplicates from df
#                     df.drop_duplicates(inplace=True)
# 
#                     # merge df and df_pivot based on index_col
#                     df_merged = merge(df, df_pivot, on=index_col, how='left')
# 
#                     # write df_merged to file
#                     self.WriteData(df_merged, filename)
                    self.WriteData(df_pivot, filename)
                except OSError:
                   print("Error while reading %s" % filename)
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
        data_frame.to_csv(join(self.output_dir,
                              output_name.replace("merged", "pivoted")),
                          sep=",",
                          index=True)
    # end WriteData


def main():
    staar_merge = "4_staar_merged"
    staar_pivot = "5_staar_pivoted"

#     for item_dir in listdir(staar_merge):
#         input_dir = join(staar_merge, item_dir)
#         output_dir = join(staar_pivot, item_dir)
#         input_dir = staar_merge
#         output_dir = staar_pivot
#         StaarPivot(input_dir, output_dir)
#         StaarPivot(input_dir, output_dir)
    StaarPivot(staar_merge, staar_pivot)
    print("Finished")

if __name__ == "__main__":
    main()
    
