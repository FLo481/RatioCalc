import numpy as np
import csv
import os

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

    # For the l=1 modes add the following
    # "LargeDS_Gauge_l m_q=1.31.txt"

    for root, dirs , files in os.walk(dirName):
        for file in files:
            if file.endswith(fileNameGauge):
                print("Reading in file " + os.path.join(root, file))
                with open(os.path.join(root, file)) as f:
                    reader = csv.reader(f, delimiter = '\t')
                    for row in reader:
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
    ratio = []
    m_ratio = []
    mut_gsquared = []
    index_temp = []
    n = 0
    m = 0

    for i in range(len(gsquared)):
        if i < m:
            continue
        else:
            for j in range(len(gsquaredgauge)):
                if gsquared[i] > 0 and gsquaredgauge[j] > 0:
                    if gsquared[i] / gsquaredgauge[j] < 1 and gsquared[i] / gsquaredgauge[j] > 0.995:
                        n += 1
                        index_temp.append(j)
                        ratio_temp.append(gsquared[i] / gsquaredgauge[j])

            #max_ratio = find_max_in_list(ratio_temp)

            for k in range(n):
                if find_max_in_list(ratio_temp) is ratio_temp[k]:
                    mut_gsquared.append(gsquaredgauge[index_temp[k]])
                    m_ratio.append(np.sqrt(mesinomsquared[i] / msquaredgauge[index_temp[k]]))

            n = 0
            max_ratio = 0
            ratio_temp = []
            index_temp = []

        m = 0

        for k in range(len(gsquared)):
                if gsquared[i] - gsquared[k] < 0.01:
                    m += 1

    return mut_gsquared, m_ratio

def ratiocalcFPLUS(dirName):

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_FPlus L=0.40.txt", "LargeDS_Gauge L=0.40.txt")

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "\FPlus_over_Gauge_L=0.40.txt", mut_gsquared, m_ratio)

    return 0

def ratiocalcGPLUS(dirName):

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_GPlus L=0.40.txt", "LargeDS_Gauge L=0.40.txt")    

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "\GPlus_over_Gauge_L=0.40.txt", mut_gsquared, m_ratio)

    return 0

def ratiocalcGMinus(dirName):

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_GMinus L=0.40.txt", "LargeDS_Gauge L=0.40.txt")

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "\GMinus_over_Gauge_L=0.40.txt", mut_gsquared, m_ratio)

    return 0

def ratiocalcFMinus(dirName):

    mesinomsquared, gsquared, msquaredgauge, gsquaredgauge = readindata(dirName, "LargeDS_FMinus L=0.40.txt", "LargeDS_Gauge_l=1 L=0.40.txt")

    mut_gsquared, m_ratio = ratiocalc(mesinomsquared, gsquared, msquaredgauge, gsquaredgauge)

    csv_writer(dirName + "\FMinus_over_Gauge_L=0.40.txt", mut_gsquared, m_ratio)

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
    #dirName = r"C:\Users\Flo\Desktop\Masterarbeit\Mathematica\CompData\Ratios"
    #SUSY
    dirName = r"C:\Users\Flo\Desktop\Masterarbeit\Mathematica\CompData\Ratios\SUSY"
    #dirName = r"/opt/RatioCalc/Ratios/SUSY"

    #ratiocalcFPLUS(dirName)
    ratiocalcGPLUS(dirName)
    #ratiocalcGMinus(dirName)
    #ratiocalcFMinus(dirName)
if __name__ == "__main__" :
    main()