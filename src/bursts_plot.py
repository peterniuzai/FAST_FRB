import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sigpyproc.Readers import FilReader
import glob
import os,sys
import sigpyproc.Utils as ut
import json
import socket


def downsample(data,f_down,t_down):
	f_step = f_down
	t_step = t_down
	d = data
	d_new_freq = np.zeros((d.shape[0]/f_step,d.shape[1]))
	d_new = np.zeros((d.shape[0]/f_step,d.shape[1]/t_step))
	for f in range(d.shape[0]/f_step):
	        d_new_freq[f,:]=d[f*f_step:(f+1)*f_step,:].sum(axis=0)
	
	
	for t in range(d.shape[1]/t_step):
	        d_new[:,t]=d_new_freq[:,t*t_step:(t+1)*t_step].sum(axis=1)
	return d_new

def time_delay(DM_range,fbot,ftop):
	'''Calculate time delay according to top frequency and bottom frequency with max DM'''
	C     = 4.148908e6 # (ms)
	t_delay   = C * DM_range[1] * (fbot**-2  -  ftop**-2) #Time delay betweent top and bottom frequency with max DM value. (ms)
	return t_delay	

#python plot_candidate.py $project,$date_obs, $fil_line, $gold_can

#plot_flag =  "20190506/"

hostname        = socket.gethostname()
hostID = int(hostname.split("x")[1])


fil_path  = "/data26/zhuww/psr_19beam_1bit/"

project		= sys.argv[1] + '/'
date_f		= sys.argv[2] + '/'
C 		= 4.148908e6 # (ms)
n_file		= int(sys.argv[3]) - 1 
cand_f		= sys.argv[4]
serv_list       = json.loads(sys.argv[5])
cand_now	= project.split('/')[0]+date_f.split('/')[0]

date_list       = sorted(glob.glob(fil_path + project+'*'))
N_day           = len(date_list)
N_serv          = len(serv_list)

#print date_list[0].split('/')[-1]
#exit()

#date_f_num	= int(date_f.split('/')[0])
#date_list_num	= json.loads(date_list)
#date_list_num	= np.array(date_list,key=lambda s:s.split('/')[-1],dtype=np.int)
#lo = np.where(date_list_num == date_f_num)
#print lo
#exit()

for i in np.arange(N_day):

   if date_f.split('/')[0] == date_list[i].split('/')[-1] and hostID == serv_list[i%N_serv]:


	print "========START============"
	print "Golden Cands:%s"%cand_f
	
#	if not os.path.exists(cand_f[:-5]):
#	       os.makedirs(cand_f[:-5])
	if os.path.getsize(cand_f) == 0:
			print cand_f, "size ==0"
			exit()
	#if cand_now in plot_flag:
	candidates	= np.loadtxt(cand_f)
	pathlist	= sorted(glob.glob(fil_path + project + date_f +'/*.fil'))
	pathlist	= sorted(pathlist,key=lambda x: x.split('_')[-2].split('-M')[-1])
	num_file	= len(pathlist)/19
	
	if candidates.size == 6:
		len_file = 1
	else:
		len_file = len(candidates)
	print "%d th Fiterbank File of Date:%s"%(n_file,date_f)
	#with open(cand_f[:-5]+'/'+cand_f.split('/')[-1].split('.')[0]+'_result.txt','w') as f_result:
	result_name = '/data26/home/nch/FAST_Miner/Gold_Mine/'+ project +  date_f + project.split('/')[0]+date_f.split('/')[0]+'_result.txt'
	with open(result_name,'a+') as f_result:
	  for row in range(len_file):
		if candidates.size > 6 :
			#print row,candidates.shape,len_file
			sample_ID = int(candidates[row,2])
			DM	  = candidates[row,3]
			BeamID	  = candidates[row,5]
			snr_heim  = candidates[row,0]
			pulse_wid = abs(2**int(candidates[row,4]-1))
			
		if candidates.size == 6 :
			#print row,candidates.shape,len_file
			sample_ID = int(candidates[2])
			DM        = candidates[3]
	                BeamID    = candidates[5]
			snr_heim  = candidates[0]
			pulse_wid = abs(2**int(candidates[4]-1))

		index_next = int(num_file*(BeamID-1)+n_file+1)
		index_last = int(num_file*(BeamID-1)+n_file-1)
		if index_next == len(pathlist):
			index_next = index_next - 1
		if index_last == -1:
			index_last = index_last + 1
		filename = pathlist[int(num_file*(BeamID-1)+n_file)]#"*M%02d_%00004d.fil"%(BeamID,n_file)
	        filename_last = pathlist[index_last]#"*M%02d_%00004d.fil"%(BeamID,n_file-1)
	        filename_next = pathlist[index_next]#"*M%02d_%00004d.fil"%(BeamID,n_file+1)
		filename = filename.split('/')[-1]
		filename_next = filename_next.split('/')[-1]
		filename_last = filename_last.split('/')[-1]
		#print "next filterbank:\n",filename_next
		#print "Last filterbank:\n",filename_last
		#print "Right Now:\n",filename
		
			
		print "File Path:", fil_path + project + date_f+filename
		
		f = FilReader(fil_path + project + date_f +'/'+ filename)
		MJD_Start = f.header.tstart
		t_rsl   = f.header.tsamp # Unit (s)
		f_rsl	= abs(f.header.foff)
		f_top	= f.header.ftop
		f_bot	= f.header.fbottom
		mjd_burst = sample_ID*t_rsl/3600/24. + MJD_Start
		sample_delay = np.int(((f_bot**-2 - f_top**-2)*C*DM)/(t_rsl*1000))	
		if sample_delay <= 15000:
			sample_delay = 15000
		

		filterbank_new_dir = "../Data/Pick_Filterbank_Data/" + project + date_f +  cand_f.split('/')[-1][:-5]+'/'
	#	filterbank_new_dir = cand_f[:-5]+"/Pick_Filterbank_Data/" 
		if not os.path.exists(filterbank_new_dir):
	                	os.makedirs(filterbank_new_dir)
	
		f_new = f.header.prepOutfile(filterbank_new_dir+str(int(row))+'.fil',nbits=32)
		if sample_ID + sample_delay < f.header['nsamples'] and sample_ID -5000 > 0:
			    	data = f.readBlock(sample_ID-5000,5000 + sample_delay)
				f_new.write(data)
		elif sample_ID + sample_delay > f.header['nsamples'] and sample_ID -5000 > 0 and os.path.exists(fil_path+ project+date_f +'/'+ filename_next):
				f_next   = FilReader(fil_path + project+date_f +'/'+ filename_next)
				data_stack = f_next.readBlock(0,sample_delay-(f.header.nsamples-sample_ID))
	    			data = f.readBlock(sample_ID-5000,f.header['nsamples']-sample_ID+5000)
				f_new.write(data)
	                        f_new.write(data_stack)
		elif sample_ID -5000 < 0 and os.path.exists(fil_path+project + date_f +'/'+ filename_last):
				data = f.readBlock(0,sample_delay+sample_ID)
				f_last = FilReader(fil_path + project + date_f +'/'+ filename_last)
				data_stack = f_last.readBlock(f.header.nsamples-(5000-sample_ID),5000-sample_ID)
	
				f_new.write(data_stack)
	                        f_new.write(data)
	
	        f_new.close()
	
		f_new = FilReader(filterbank_new_dir +'%d.fil'%row)
	
		data = f_new.readBlock(0,sample_delay + 5000)
			
		dedata = data.dedisperse(DM)

	
#		if snr_heim < 12:
#			fdown = 128
#			tdown = 40
#		elif 20  > snr_heim > 12 :
#			fdown = 64
#			tdown = 20
#		else:
#			fdown = 32
#			tdown = 10
		if snr_heim < 12:
                       fdown = 128
                       tdown = pulse_wid
                elif 20  > snr_heim > 12 :
                       fdown = 64
                       tdown = pulse_wid
                else:
                       fdown = 32
                       tdown = pulse_wid
		data_d = downsample(data,fdown,tdown)
	#		print data_d.shape
		dedata_d = downsample(dedata,fdown,tdown)

		
		for N_rfi in range(np.int(round(data_d.shape[0]*0.1))):
			lo = np.where(data_d.sum(axis=1)==data_d.sum(axis=1).max())
			data_d[lo[0][0],:] = np.median(data_d)
			dedata_d[lo[0][0],:] = np.median(dedata_d)
			
			

	

		#Notification Line

                C = 4.148908e6 # (ms)
                line_f = np.linspace(f_top,f_bot,data_d.shape[0])
		scale_f = int(round(sample_delay/15000.))
                line1_t = sample_ID - 800*scale_f + np.round(((np.power(line_f,-2) - f_top**-2)*C*DM)/(t_rsl*1000))
		line2_t = sample_ID + 800*scale_f + np.round(((np.power(line_f,-2) - f_top**-2)*C*DM)/(t_rsl*1000))

		x_axis = np.linspace(sample_ID-5000,sample_ID+sample_delay,data_d.shape[1])
		y_axis = np.linspace(f_top,f_bot,data_d.shape[0])
	
		#plt.figure(figsize=[15,13])
		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,figsize=[13,12])
		textplot = 'DM:'+str(DM)+' SNR:'+str(snr_heim)+' Date:'+project.split('/')[0]+date_f.split('/')[0]+' MJD:'+str(mjd_burst)+'\nFile:'+filename+'  SampleID:%d'%sample_ID
		fig.text(0.31,0.95,textplot,fontsize=15,bbox=dict(facecolor='lightblue'),color='red')
		ax1.set_title("Raw Data")
		ax1.set_xlabel("Time sample")
		ax1.set_ylabel("Frequency(MHz)")
		#plt.axvline(sample_ID+1000,color='r',linestyle='dashed')
		ax1.axvline(sample_ID,color='r',linestyle='dashed')
		ax1.set_ylim(y_axis.min(),y_axis.max())
		ax1.set_xlim(x_axis.min(),x_axis.max())
	#	plt.pcolormesh(x_axis,y_axis,data_d,vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
		ax1.pcolormesh(x_axis,y_axis,data_d,cmap='gray_r',vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
		ax1.plot(line1_t,line_f,color='y',linestyle='dashed')
		ax1.plot(line2_t,line_f,color='y',linestyle='dashed')
		#ax1.colorbar()
			
		ax2.set_title("Dedispersed Data")
		ax2.set_xlabel("Time sample")
		ax2.set_ylabel("Frequency(MHz)")
		ax2.axvline(sample_ID+300*scale_f,color='r',linestyle='dashed')
		ax2.axvline(sample_ID-300*scale_f,color='r',linestyle='dashed')
		ax2.set_ylim(y_axis.min(),y_axis.max())
		ax2.set_xlim(x_axis.min(),x_axis.max())
		ax2.pcolormesh(x_axis,y_axis,dedata_d,vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
		#plt.pcolormesh(x_axis,y_axis,dedata_d,cmap='gray_r',vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
		#ax2.colorbar()
			
		ax3.set_title("Raw Data Integration")
		ax3.set_xlabel("Time sample")
		ax3.set_ylabel("Intensity")
		ax3.axvline(sample_ID,color='r',linestyle='dashed')
		ax3.set_ylim(data_d.sum(axis=0).min(),data_d.sum(axis=0).max())
		ax3.set_xlim(x_axis.min(),x_axis.max())
		ax3.plot(x_axis,data_d.sum(axis=0))
			
		ax4.set_title("Dedispersed Data Integration")
		ax4.set_xlabel("Time sample")
		ax4.set_ylabel("Intensity")
		ax4.axvline(sample_ID,color='r',linestyle='dashed')
		ax4.set_ylim(dedata_d.sum(axis=0).min(),dedata_d.sum(axis=0).max())
		ax4.set_xlim(x_axis.min(),x_axis.max())
		ax4.plot(x_axis,dedata_d.sum(axis=0))	
		plot_dir = cand_f[:-5]#+'_new/'

	        #if not os.path.exists(plot_dir):
        	#       os.makedirs(plot_dir)
		
		#plot_name = project.split('/')[0]+date_f.split('/')[0]+'_'+ str(n_file)+'th_'+str(sample_ID)
		plot_name = str(mjd_burst)+'.png'
		f_result.write(project.split('/')[0]+date_f.split('/')[0]+' '+ str(n_file-1)+' '+str(sample_ID)+' '+ str(mjd_burst) +' '+str(DM)+' '+ str(snr_heim)+' ' + str(int(BeamID))+'\n' )
		fig.tight_layout(h_pad=1,w_pad=1,rect=[0.,0,1,0.95])#pad=0.2, w_pad=0.3, h_pad=0.5)
		plt.savefig(plot_dir+'_MJD:'+plot_name) 
		plt.close()
	print "---------END-------------\n\n"
	break
#	plt.show()
#	exit()

