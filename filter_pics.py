import time,os,shutil
src_dir='S:\\Shweta\\Photoes\\2015\\Thailand'
#tmp=Path(src_dir)
tmp=time.strftime('%d_%m_%Y_%H%M%S')
print('filtered files directory name = ',tmp)
	


file=open('thailand.txt','r')
to_filter=[]
if not file:
	print('file doesn\'t exist')
	exit(0)
	
for line in file:
		to_filter.append(line.strip())	

print('filter list = ',to_filter)		
	
dest_dir=src_dir+'\\'+tmp
os.mkdir(dest_dir)
files=os.listdir(src_dir)
print(files)
for file in files:
	if os.path.isfile(src_dir+'\\'+file) and file.endswith('.JPG'):
		print('comparing '+file)
		for pattern in to_filter:
			if pattern.startswith('#'):
				continue
			if file.find(pattern+'.JPG')!=-1:
				print('copying ... '+file)
				shutil.copy(src_dir+'\\'+file,dest_dir)





#file.close()	
print('dir name',tmp)
