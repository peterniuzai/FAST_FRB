import matplotlib
#matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from sigpyproc.Readers import FilReader
import glob
import os,sys
import sigpyproc.Utils as ut


def RFI_clean(data):
	for i in range(100):
		freq_sum = data.sum(axis=1)
		lo = np.where(freq_sum == freq_sum.max())
		if lo[0][0] < 3000:
			data[lo[0][0]-5:lo[0][0]+5,:] = data.mean()
#	plt.plot(freq_sum)
#	plt.show()
	return data	

def downsample(data,f_down,t_down):
	f_step = f_down
	t_step = t_down
	d = data
	d_new_freq = np.zeros((d.shape[0]/f_step,d.shape[1]))
	d_new = np.zeros((d.shape[0]/f_step,d.shape[1]/t_step))
#	print d_new.shape
	for f in range(d.shape[0]/f_step):
	        d_new_freq[f,:]=d[f*f_step:(f+1)*f_step,:].sum(axis=0)
	
#	print d_new_freq.shape
	
	for t in range(d.shape[1]/t_step):
	        d_new[:,t]=d_new_freq[:,t*t_step:(t+1)*t_step].sum(axis=1)
	return d_new
	

#python plot_candidate.py $project,$date_obs, $fil_line, $gold_can

#plot_flag =  "20190506/"
fil_path  = "/data5/zhuww/psr_19beam_1bit/"


project		= '201905/'
date_f		= '20/'
n_file		=  399 
#if cand_now in plot_flag:

sample_ID = 81232
DM	  = 1229.82
BeamID	  = 2
snr_heim  = 9.73
		
#print row,candidates.shape,len_file
filename = 'Dec-1124_arcdrift+23.4-M02_0400.fil'
print "File Path:", fil_path + project + date_f+filename
	
f = FilReader(fil_path + project + date_f +'/'+ filename)
MJD_Start = f.header.tstart
t_rsl 	= f.header.tsamp
mjd_burst = sample_ID*t_rsl/3600/24. + MJD_Start
data = f.readBlock(sample_ID-5000,20000)
#print data.dtype,data.shape,data[2000:2100]
#d = np.float32(data)

#np.save("frbcandidate_DM1229_82.npy",data)
#print 'Save Done!'
#exit()
#data = RFI_clean(data)
dedata = data.dedisperse(DM)

if snr_heim < 12:
	fdown = 128
	tdown = 40
elif 20  > snr_heim > 12 :
	fdown = 64
	tdown = 20
else:
	fdown = 32
	tdown = 10
fdown = 64
tdown = 10
data_d = downsample(data,fdown,tdown)
#		print data_d.shape
dedata_d = downsample(dedata,fdown,tdown)

x_axis = np.linspace(sample_ID-5000,sample_ID+15000,data_d.shape[1])
y_axis = np.linspace(1499,1000,data_d.shape[0])

	#plt.figure(figsize=[15,13])
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,figsize=[13,12])
textplot = 'DM:'+str(DM)+' SNR:'+str(snr_heim)+' Date:'+project.split('/')[0]+date_f.split('/')[0]+' MJD:'+str(mjd_burst)+'\nFile:'+filename+'  SampleID:%d'%sample_ID
fig.text(0.30,0.95,textplot,fontsize=15,bbox=dict(facecolor='lightblue'),color='red')
ax1.set_title("Raw Data")
ax1.set_xlabel("Time sample")
ax1.set_ylabel("Frequency(MHz)")
#plt.axvline(sample_ID+1000,color='r',linestyle='dashed')
ax1.axvline(sample_ID,color='r',linestyle='dashed')
ax1.set_ylim(y_axis.min(),y_axis.max())
ax1.set_xlim(x_axis.min(),x_axis.max())
#	plt.pcolormesh(x_axis,y_axis,data_d,vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
ax1.pcolormesh(x_axis,y_axis,data_d,vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
	#ax1.colorbar()
		
ax2.set_title("Dedispersed Data")
ax2.set_xlabel("Time sample")
ax2.set_ylabel("Frequency(MHz)")
ax2.axvline(sample_ID+1000,color='r',linestyle='dashed')
ax2.axvline(sample_ID-1000,color='r',linestyle='dashed')
ax2.set_ylim(y_axis.min(),y_axis.max())
ax2.set_xlim(x_axis.min(),x_axis.max())
ax2.pcolormesh(x_axis,y_axis,dedata_d,vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
#plt.pcolormesh(x_axis,y_axis,dedata_d,cmap='gray_r',vmax=data_d.max()-data_d.std(),vmin=data_d.min()+data_d.std())
#ax2.colorbar()
		
ax3.set_title("Raw Data Integration")
ax3.set_xlabel("Time sample")
ax3.set_ylabel("Intensity")
ax3.axvline(sample_ID,color='r',linestyle='dashed',label='zhu')
ax3.set_ylim(data_d.sum(axis=0).min(),data_d.sum(axis=0).max())
ax3.set_xlim(x_axis.min(),x_axis.max())
ax3.plot(x_axis,data_d.sum(axis=0))
		
ax4.set_title("Dedispersed Data Integration")
ax4.set_xlabel("Time sample")
ax4.set_ylabel("Intensity")
ax4.axvline(sample_ID,color='r',linestyle='dashed',label='zhu')
ax4.set_ylim(dedata_d.sum(axis=0).min(),dedata_d.sum(axis=0).max())
ax4.set_xlim(x_axis.min(),x_axis.max())
ax4.plot(x_axis,dedata_d.sum(axis=0))	
#plot_dir = cand_f[:-5]+'/'
#plot_name = project.split('/')[0]+date_f.split('/')[0]+'_'+ str(n_file)+'th_'+str(sample_ID)
fig.tight_layout(h_pad=1,w_pad=1,rect=[0.,0,1,0.95])#pad=0.2, w_pad=0.3, h_pad=0.5)
#plt.savefig('test.png') 
#	plt.close()
plt.show()
#	exit()

