ls /home/rooney/Data\ mining\ dataset/UDI-TwitterCrawl-Aug2012-Tweets/tweets/  > /home/rooney/DATASET/file_list.txt
file_name=/home/rooney/DATASET/file_list.txt 
i=0;
count=1000;
touch  /home/rooney/Data\ mining\ dataset/CleanData/CleanedData/user_list.txt
while read line ;do
      if [ $i -lt $count ]
	       then
                 #echo $line >> /home/rooney/Data\ mining\ dataset/CleanData/CleanedData/user_list.txt  #printing the user_list
        	#cp /home/rooney/Data\ mining\ dataset/UDI-TwitterCrawl-Aug2012-Tweets/tweets/$line   /home/rooney/DATASET/
              touch /home/rooney/dataMiningPackage/DATASET/$line
              touch /home/rooney/dataMiningPackage/DATASET/temp
              cat /home/rooney/dataMiningPackage/DATASET/$line | tr A-Z a-z > /home/rooney/dataMiningPackage/DATASET/temp
              mv /home/rooney/dataMiningPackage/DATASET/temp      /home/rooney/dataMiningPackage/DATASET/$line
              grep -e "Text:" /home/rooney/Data\ mining\ dataset/UDI-TwitterCrawl-Aug2012-Tweets/tweets/$line > /home/rooney/dataMiningPackage/DATASET/$line 
              sed -i 's/Text://g' /home/rooney/dataMiningPackage/DATASET/$line 
              #cat  home/rooney/Data\ mining\ dataset/CleanData/CleanedData/$line 
              #cat /home/rooney/Data\ mining\ dataset/CleanData/CleanedData/sample.txt 
              #mv /home/rooney/Data\ mining\ dataset/CleanData/CleanedData/sample.txt /home/rooney/Data\ mining\ dataset/CleanData/CleanedData/$line
              #cat /home/rooney/Data\ mining\ dataset/CleanData/CleanedData/\$line 
        #echo $line
      fi
i=$((i + 1))
done < /home/rooney/DATASET/file_list.txt
