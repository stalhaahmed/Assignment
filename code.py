
import requests
from datetime import datetime
import time

s_SeqLast="Seq"
i_Loop=int(1)
f_diff_time = float()
f_min_time = float()
f_max_time = float()
f_avg_time = float()

s_Last_date_time=str("")
s_Curr_date_time=str("")


file_handle = open("Task_seq_n_time.txt", "a")
file_handle_extra = open("Task_seq_duration.txt", "a")
data = {
       "method": "server_info"
       }

#in loop api call start
while (i_Loop < 501):

        r = requests.post(
            url="http://s1.ripple.com:51234/",
            json=data
        )

        # extracting response text  
        Seq_String = str(r.content) 
        
        # Parsing Time
        i_SeqTime = Seq_String.find('\"time\"')+8

        s_TimeStr=Seq_String[i_SeqTime:i_SeqTime+27]
        #print("\n\nTime: %s"%s_TimeStr, "\nindex ",i_SeqTime)

        # parsing Sequence
        i_SeqIndexStart = Seq_String.find('\"seq')+6
        i_SeqIndexEnd = Seq_String.find('\"validation_quorum')-2

        s_Seq=Seq_String[i_SeqIndexStart:i_SeqIndexEnd]
        #print("\n\nSeq: %s"%s_Seq, "\nindex ",i_SeqIndexStart)

        #date conversion
        date_time_obj = datetime.strptime(s_TimeStr, '%Y-%b-%d  %H:%M:%S.%f')
        if (i_Loop == 1):
          s_Last_date_time =date_time_obj.strftime("%Y-%b-%d  %H:%M:%S.%f")
        s_Curr_date_time=date_time_obj.strftime("%Y-%b-%d  %H:%M:%S.%f")
        s_TimeStr=date_time_obj.strftime("%d/%m/%y.%H:%M:%S")
        

        if (s_Seq != s_SeqLast): #if start
          i_Loop = i_Loop + 1

          Diff_date_time = datetime.strptime(s_Curr_date_time, '%Y-%b-%d  %H:%M:%S.%f') - datetime.strptime(s_Last_date_time, '%Y-%b-%d  %H:%M:%S.%f')
          f_diff_time = Diff_date_time.microseconds / 1000000
          f_diff_time = f_diff_time + Diff_date_time.seconds

          if i_Loop <= 4:
            f_max_time = f_diff_time
            f_min_time = f_diff_time

          if f_max_time < f_diff_time:
            f_max_time = f_diff_time

          if f_min_time > f_diff_time:
            f_min_time = f_diff_time
        
          s_SeqLast = s_Seq
          sNewData=s_TimeStr+" "+s_SeqLast+"\n"
          file_handle.writelines(sNewData)          # To write sequence against actual time

          sNewData=str('%1.6f'%f_diff_time)
          sNewData=sNewData +" "+s_SeqLast+"\n"
          file_handle_extra.writelines(sNewData)    # To write time taken by each sequence
          s_Last_date_time =date_time_obj.strftime("%Y-%b-%d  %H:%M:%S.%f")
           #if end
        time.sleep(0.8)
        #in loop api call end
        
f_avg_time = (f_max_time + f_min_time) / 2
print("\nmax value: %f"%f_max_time)
print("\nmin value: %f"%f_min_time)
print("\navg value: %f"%f_avg_time)
sNewData="\nMaximum value: " + str(f_max_time) + "\nMinimum value: " + str(f_min_time) + "\nAverage value: " + str(f_avg_time) 
file_handle_extra.writelines(sNewData)    # To write time taken by each sequence
          

file_handle_extra.close()
file_handle.close()
