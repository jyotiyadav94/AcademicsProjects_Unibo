from os import listdir, mkdir
#listdir: return the list containing the names of the entries given by the path
#mkdir: Create a directory named path with numeric mode mode.
from os.path import isfile, join, exists
#isfile: return true if the file exist
#join: return the concatenation of path components
#exists: return True if path refers to an existing path or an open file descriptor


def write_in_dzn(f, name_var, value_var):
    '''

    :param f:  name of instance in .dzn
    :param name_var: name of the variable
    :param value_var: is the variable
    :return: This function writes all the variables
             in instances files where instances are converted from .txt to .dzn
    '''
    f.write(name_var + ' = ' + str(value_var) + ";\n")


in_path = "../instances/"
dzn_folder_path = "../CP/instances_dzn/"
dzn_file_name = "ins-"
dzn_extension = ".dzn"

# for loop to get input files' name
files_name=[]
for f in listdir(in_path):
    if isfile(join(in_path, f)):
        files_name.append(f)

#if the directory defined in 'out_path' doesn't exist tyhen one it's created
if not exists(dzn_folder_path):
    mkdir(dzn_folder_path)

#each txt file is read and converted in dzn format
for fn in files_name:
    ins = fn.split('.')[0].split('-')[1]
    in_file = open(in_path + fn, "r")
    w = int(in_file.readline())
    n_circuits = int(in_file.readline())
    x=[]
    y=[]
    for i in range(n_circuits):
        circuit = in_file.readline().split(' ')
        x.append(int(circuit[0]))
        y.append(int(circuit[1]))
    #Once all variables have been defined,
    #they will be written to the output instances_dzn files with the extension 'dzn'.
    ins_dzn_file = open(dzn_folder_path + dzn_file_name + ins + dzn_extension, "w")
    write_in_dzn(ins_dzn_file, "fixed_width", w)
    write_in_dzn(ins_dzn_file, "n_circuits", n_circuits)
    write_in_dzn(ins_dzn_file, "horizontal_dim", x)
    write_in_dzn(ins_dzn_file, "vertical_dim", y)

