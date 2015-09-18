'''
Created on 17.09.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import listdir
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat


class AddStateRow:
    data_dir_state = "InputFiles/_AEIS_State"
    data_dir_district = "InputFiles/AEIS_District"
    data_dir_output = "OutputFiles"

    def __init__(self):
        self.Process()
    # end __init__

    def Process(self):
        print ("Processing started")
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
                    district_filename = splitext(district_item)[0]

                    # Find proper state file
                    state_file_path = self.FindProperStateFile(
                                                district_filename)
                    
                    if state_file_path is not None:
                        data_frame_output = self.ConcatenateFiles(
                                                district_file_path,
                                                state_file_path)
                        self.WriteData(data_frame_output, district_item)            
    # end Process

    def FindProperStateFile(self, district_filename):
        """
        It returns state file that corresponds to district filename.
        If corresponding file is not found, return value is None
        """
        for state_item in listdir(self.data_dir_state):
            # Check only .csv files
            if splitext(state_item)[1] == ".csv":
                state_file_path = join(self.data_dir_state, state_item)
                #get full name of the state file
                state_filename = splitext(state_item)[0]
                tmp = state_filename.replace("state", "district")
                if district_filename == tmp:
                    return state_file_path
        else:
            print("There is no corresponding file for %s" % district_filename)
            return None
    # end FindProperStateFile

    def ConcatenateFiles(self,
                         district_file_path,
                         state_file_path):
        # read district .csv file
        data_frame_district = read_csv(district_file_path,
                                       delimiter=",",
                                       header=0)
        # read state .csv file
        data_frame_state = read_csv(state_file_path,
                                       delimiter=",",
                                       header=0)

        # replace column names in the state data frame
        columns = dict()
        for col in data_frame_state.columns:
            if col not in ("DISTRICT", "YEAR"):
                columns[col] = "D" + col[1:]
        data_frame_state.rename(columns=columns, inplace=True)

        # concatenate district and state data frames
        data_frame_output = concat((data_frame_district,
                                    data_frame_state),
                                    ignore_index=True)
        return data_frame_output
    # end ConcatenateFiles

    def WriteData (self,
                   data_frame,
                   output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """

        print ("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.data_dir_output, output_name),
                          sep=",",
                          index = False)
    # end WriteData

def main():
    AddStateRow()
    print("Finished")

if __name__ == "__main__":
    main()
