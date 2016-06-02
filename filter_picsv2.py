import time,os,shutil
#src_dir='R:\\Pictures\\Mysore'
#tmp=Path(src_dir)
#tmp=time.strftime('%d_%m_%Y_%H%M%S')
#print('filtered files directory name = ',tmp)

cur_dir=None
dest_dir=None
files=None

def change_current_dir(line):
	tmp=line.split('=')
	global cur_dir
	cur_dir=tmp[1].strip()
	print ('switching to src dir ',cur_dir)
	global files
	files=os.listdir(cur_dir)
	print(files)
	
def change_dest_dir(line):
	tmp=line.split('=')
	global dest_dir
	dest_dir=tmp[1].strip()
	print ('switching to dest dir ',dest_dir)
	if os.path.exists(dest_dir):
		return
	else:
		os.mkdir(dest_dir)
		
def process(e):

	if e.startswith('#'):
		return
	global files,cur_dir	
	for file in files:
	    	
		if not file.startswith('.') and os.path.isfile(cur_dir+'\\'+file) and ( file.endswith('.jpg') or file.endswith('.JPG')):
			print('comparing = '+file+' with pattern = ' +e)
			if file.find(e)!=-1:
				print('copying ... '+file)
				shutil.copy(cur_dir+'\\'+file,dest_dir)
		

if __name__=="__main__":		
	file=open('us.txt','r')
	to_filter=[]
	if not file:
		print('file doesn\'t exist')
		exit(0)
		
	for line in file:
			if line.startswith('src_folder'):
				change_current_dir(line.strip())
				#print("files = "+ files)
			elif line.startswith('folder'):
				change_dest_dir(line.strip())
			else:
				process(line.strip())	
