'''
Created on 19.10.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat

DS = {'district': 'd',
      'state': 's'}

class StaarMerge:
    
    script_name = "StaarMerge"
    Columns = list()

    inputs = {"state": (join("..", "Inputs", "staar", "state"),
                         "%sState" % script_name),
              "district": (join("..", "Inputs", "staar", "district"),
                           "%sDistrict" % script_name)
              }

    def __init__(self):
        # self.CleanOutput()
        # self.ReadData()
        self.Merge()
    # end __init__

    def CleanOutput(self):
        # TODO
        # add removing of merged files
        print("Clean Output")
        for key, value in self.inputs.items(): 
            if exists(value[1]):
                for item in listdir(value[1]):
                    remove(join(value[1], item))
                print("\t %s output dir cleaned: %s" % (key, value[1]))
    # end CleanOutput

    def ReadData(self):
        print("\nRead Data")
        for ds, value in self.inputs.items():
            if not path.exists(value[0]):
                print("\t Data Directory Does Not Exist %s" % value[0])
                exit()
            else:
                # List directory containing the .csv files
                for item in listdir(value[0]):

                    # Check the extension of the files,
                    # so only .csv files will be considered
                    name_of_file = path.splitext(item)[0]
                    if(path.splitext(item)[1] == ".csv"):
                        file_path = path.join(value[0], item)

                        # Pandas.read_csv method returns DataFrame object
                        try:
                            data_frame = read_csv(file_path,
                                              delimiter=",",
                                              header=0,
                                              low_memory=False)
                            if ds == 'state':
                                data_frame.insert(0, 'DISTRICT', 1)
                            self.WriteData(data_frame, item, value[1])
                        except:
                            print("Error while reading %s" % item)
                            print("Columns: %s\n" % adjusted_columns)
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name,
                  output_dir):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(output_dir):
            mkdir(output_dir)
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(output_dir, output_name),
                          sep=",",
                          index=False)
    # end WriteData

    def Merge(self):
        print("Start merging")

        # Read Inputs
        for key, value in self.inputs.items():
            data_frames = list()
            for item in listdir(value[1]):
                if path.splitext(item)[1] == ".csv":
                    f = path.join(value[1], item)
                    data_frames.append(read_csv(f,
                                                delimiter=",",
                                                header=0,
                                                low_memory=False))
            data =  concat(data_frames)

            # Write to output
            merged_file = join("..",
                               "MergedFiles",
                               "%s_%s.csv" % (self.script_name, key))
            data.to_csv(merged_file, sep=",", index = False)
            print("\t %s files merged into: %s" % (key, merged_file))
    # end Merge

def main():
    StaarMerge()
    print("Finished")

if __name__ == "__main__":
    main()
