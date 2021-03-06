import numpy as np
import csv
import os

#from numpy.lib.ufunclike import isposinf

def find_max_in_list(example_list):

    maximum = 0
    temp = 0

    if len(example_list) is 1:
       maximum = example_list[0]
    else:
       for f in range(len(example_list)):
          for l in range(len(example_list)):
             if f is l:
                continue
             elif example_list[f] > example_list[l]:
                temp = example_list[f]
                if temp > maximum:
                   maximum = temp

    return maximum

def readindata(dirName, fileNameMesino, fileNameGauge):

    mesinomsquared = []
    gsquared = []
    msquaredgauge = []
    gsquaredgauge = []

    for root, dirs , files in os.walk(dirName):
        for file in files:
            if file.endswith(fileNameGauge):
                print("Reading in file " + os.path.join(root, file))
                with open(os.path.join(root, file)) as f:
                    reader = csv.reader(f, delimiter = '\t')
                    for row in reader:
                        if float(row[1]) > 0:
                        #print(row[0])
                        #print(row[1])
                            msquaredgauge.append(row[0])
                            gsquaredgauge.append(row[1])

    f.close()

    msquaredgauge = list(map(float, msquaredgauge))
    gsquaredgauge = list(map(float, gsquaredgauge))

    for root, dirs , files in os.walk(dirName):
       for file in files:
           if file.endswith(fileNameMesino):
               print("Reading in file " + os.path.join(root, file))
               with open(os.path.join(root, file)) as f:
                   reader = csv.reader(f, delimiter = '\t')
                   for row in reader:
                      #print(row[0])
                      #print(row[1])
                      if float(row[1]) > 0 and float(row[1]) <= gsquaredgauge[0]:
                        mesinomsquared.append(row[0])
                        gsquared.append(row[1])
 
    f.close()

    mesinomsquared = list(map(float, mesinomsquared))
    gsquared = list(map(float, gsquared))

    return mesinomsquared, gsquared, msquaredgauge, gsquaredgauge

def ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge):

    ratio_temp = []
    m_ratio = []
    mut_gsquared = []
    index_temp = []
    max_ratio = 0

    for i in range(len(gsquared)):
        for j in range(len(gsquaredgauge)):
        #gsquared and gsquaredgauge have to agree within a 0.5% margin
            if gsquared[i] / gsquaredgauge[j] < 1 and gsquared[i] / gsquaredgauge[j] > 0.995:
                index_temp.append(j)
                ratio_temp.append(gsquared[i] / gsquaredgauge[j])
        
        #safe the max ration in a variable for less runtime
        max_ratio = find_max_in_list(ratio_temp)
            
        #the maximum (best agreement within the 0.5% margin) is searched for
        for k in range(len(index_temp)):
            if max_ratio is ratio_temp[k]:
                #check whether there is already the same gsquared value in the mut_gsquared array
                if gsquaredgauge[index_temp[k]] not in mut_gsquared:
                    mut_gsquared.append(gsquaredgauge[index_temp[k]])
                    m_ratio.append(np.sqrt(mesinomsquared[i] / msquaredgauge[index_temp[k]]))

        max_ratio = 0         
        ratio_temp = []
        index_temp = []
                    
    return mut_gsquared, m_ratio

def ratiocalcFPLUS(dirName):

    #For the SUSY datasets the naming scheme is LargeDS_"Mode" L="UV quark mass".txt and for the non-SUSY ones LargeDS_"Mode" m_q="UV quark mass".txt

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_FPlus m_q=0.40.txt", "LargeDS_Gauge m_q=0.40.txt")

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "/FPlus_over_Gauge m_q=0.40.txt", mut_gsquared, m_ratio)

    return 0

def ratiocalcGPLUS(dirName):

    #For the SUSY datasets the naming scheme is LargeDS_"Mode" L="UV quark mass".txt and for the non-SUSY ones LargeDS_"Mode" m_q="UV quark mass".txt

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_GPlus m_q=0.40.txt", "LargeDS_Gauge m_q=0.40.txt")    

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "/GPlus_over_Gauge m_q=0.40.txt", mut_gsquared, m_ratio)

    return 0

def ratiocalcGMinus(dirName):

    #For the SUSY datasets the naming scheme is LargeDS_"Mode" L="UV quark mass".txt and for the non-SUSY ones LargeDS_"Mode" m_q="UV quark mass".txt

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_GMinus m_q=0.40.txt", "LargeDS_Gauge m_q=0.40.txt")

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "/GMinus_over_Gauge m_q=0.40.txt", mut_gsquared, m_ratio)

    return 0

def ratiocalcFMinus(dirName):

    #For the SUSY datasets the naming scheme is LargeDS_"Mode" L="UV quark mass".txt and for the non-SUSY ones LargeDS_"Mode" m_q="UV quark mass".txt

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_FMinus m_q=10^-6.txt", "LargeDS_Gauge_l=1 m_q=10^-6.txt")

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "/FMinus_over_Gauge m_q=10^-6.txt", mut_gsquared, m_ratio)

    return 0

def csv_writer(filename, mut_gsquared, m_ratio):

    #mut_gsquared = list(map(str, mut_gsquared))
    #m_ratio = list(map(str, m_ratio))
    mut_gsquared_temp = ''
    m_ratio_temp = ''

    with open(filename, 'w', newline='\n') as file:
        writer = csv.writer(file)
        for i in range(len(m_ratio)):
            mut_gsquared_temp = str(mut_gsquared[i])
            m_ratio_temp = str(m_ratio[i])
            #print(mut_gsquared_temp + "\t" + m_ratio_temp)
            writer.writerow([mut_gsquared_temp] + [m_ratio_temp])

    print("Data written to file %s" % filename)

    file.close()

    return 0

def csv_writer2(filename, mut_gsquared, m_ratio, m_FermMode, m_Gauge):

    #mut_gsquared = list(map(str, mut_gsquared))
    #m_ratio = list(map(str, m_ratio))
    mut_gsquared_temp = ''
    m_ratio_temp = ''
    m_FermMode_temp = ''
    m_Gauge_temp = ''

    with open(filename, 'w', newline='\n') as file:
        writer = csv.writer(file)
        for i in range(len(m_ratio)):
            mut_gsquared_temp = str(mut_gsquared[i])
            m_ratio_temp = str(m_ratio[i])
            m_FermMode_temp = str(m_FermMode[i])
            m_Gauge_temp = str(m_Gauge[i])
            #print(mut_gsquared_temp + "\t" + m_ratio_temp)
            writer.writerow([mut_gsquared_temp] + [m_ratio_temp] + [m_FermMode_temp] + [m_Gauge_temp])

    print("Data written to file %s" % filename)

    file.close()

    return 0

def main():
    #nonSUSY
    #dirName = r"C:\Users\Flo\Desktop\Masterarbeit\Mathematica\CompData\Ratios\non-SUSY"
    dirName = r"/home/flo/Mathematica_data/CompData/Ratios/non-SUSY"
    #SUSY
    #dirName = r"C:\Users\Flo\Desktop\Masterarbeit\Mathematica\CompData\Ratios\SUSY"
    #dirName = r"/home/flo/Mathematica_data/CompData/Ratios/SUSY"

    ratiocalcFPLUS(dirName)
    ratiocalcGPLUS(dirName)
    ratiocalcGMinus(dirName)
    #ratiocalcFMinus(dirName)
if __name__ == "__main__" :
    main()