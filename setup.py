#!/usr/bin/env python
import sys, os, itertools, tempfile, shutil, glob, subprocess, re, pickle

#___PROJECT__PREFIX__NAME:   *crdir*.dac130
crdir='amb105b.'

#___MOLECULE___configurations_______
mlist=['da','ee','el','le','oo']        # potentials--> to be generated
molec=[mlist[0]]                        # can use [0],[1] ... [n]
ts   ='2.0'                             # 0.5, 1.0, 2.0
vels =['3']                             # ['1','3','4'] | ['4','5']
x    ={'1':2,'2':2,'3':14,'4':4,'5':3}  # duplicates--> 03.00, 03.01, 03.02
environ=['01.vac','02.imp','03.exp']    # ['01.vac']  |  ['01.vac','03.exp']
zcrd ='zc16'                            # z constraint  (smd.tcl)
envdist={'01.vac':zcrd,'02.imp':zcrd,'03.exp':zcrd} # i.e. '01.vac':zc7...
langevD='5'                             # langevin Damping: 0.2, 1, 5

#___GATE_______configurations_______
gate ='ggate'                           # 'ggate' or 'steele'
cn   ='1'                               # ppn request
comp ='cpu'                             # gpu or cpu        !TESLA: always 1
wallt='mwt'                             # swt=72 hrs, mwt=368 hrs, lwt=720 hrs
queue='workq'                           # tg_ 'short'72 'workq'720 'standby-8'

#_______<<<<<<   NO MORE CHANGES REQUIRED   >>>>>>____________________________
zdictn ={'zc1': 10.0,'zc2': 10.2,'zc3': 10.4,'zc4': 10.6,'zc5': 10.8,
         'zc6': 11.0,'zc7': 11.2,'zc8': 11.4,'zc9': 11.6,'zc10':11.8,
         'zc11':12.0,'zc12':12.2,'zc13':12.4,'zc14':12.6,'zc15':12.8,
         'zc16':13.0,'zc17':13.2,'zc18':13.4,'zc19':13.6,'zc20':13.8}
zlabel ={'zc1':'c100','zc2':'c102','zc3':'c104','zc4':'c106','zc5':'c108',
         'zc6':'c110','zc7':'c112','zc8':'c114','zc9':'c116','zc10':'c118',
         'zc11':'c120','zc12':'c122','zc13':'c124','zc14':'c126','zc15':'c128',
         'zc16':'c130','zc17':'c132','zc18':'c134','zc19':'c136','zc20':'c138'}
configf=['job.sh','go.py','smd.in','dist.RST','expavg.py']
selgate={'ggate':{'job':'job-gg.sh','go':'go-g.py'},
         'steele':{'job':'job-st.sh','go':'go-st.py'}}
confign={'1':{'gpu':'nodes=1:ppn=1:gpus=1:TESLA','cpu':'nodes=1:ppn=1'},
         '2':{'gpu':'nodes=1:ppn=2:gpus=1:TESLA','cpu':'nodes=1:ppn=2'},
         '3':{'gpu':'nodes=1:ppn=3:gpus=1:TESLA','cpu':'nodes=1:ppn=3'},
         '4':{'gpu':'nodes=1:ppn=4:gpus=1:TESLA','cpu':'nodes=1:ppn=4'},
         '5':{'gpu':'nodes=1:ppn=5:gpus=1:TESLA','cpu':'nodes=1:ppn=5'},
         '6':{'gpu':'nodes=1:ppn=6:gpus=1:TESLA','cpu':'nodes=1:ppn=6'},
         '7':{'gpu':'nodes=1:ppn=7:gpus=1:TESLA','cpu':'nodes=1:ppn=7'},
         '8':{'gpu':'nodes=1:ppn=8:gpus=1:TESLA','cpu':'nodes=1:ppn=8'},
       '16':{'gpu':'nodes=1:ppn=16:gpus=1:TESLA','cpu':'nodes=1:ppn=16'}}
configw={'swt':'walltime=72:00:00','mwt':'walltime=368:00:00',
         'lwt':'walltime=720:00:00'}
configq={'short':'tg_short','workq':'tg_workq',
         'standby-8':'tg_standby-8'}
confige={'1':'v1000','2':'v100','3':'v10','4':'v1','5':'vp1'}
envdir ={'01.vac':'maindir-v','02.imp':'maindir-i','03.exp':'maindir-e'}
strdir ={'01.vac':'08.struc-equil.v','02.imp':'08.struc-equil.i',
         '03.exp':'08.struc-equil.e'}
tstep  ={'0.5':0.5,'1.0':1.0,'2.0':2.0}
dictpf ={'1':1,'2':1,'3':50,'4':100,'5':500}
setup  ={'1':{'vel':0.002,'steps':10000,'dcd':100,'howmany':99,'freq':50},
      '2':{'vel':0.0002,'steps':100000,'dcd':1000,'howmany':48,'freq':50},
      '3':{'vel':0.00002,'steps':1000000,'dcd':10000,'howmany':30,
                                                              'freq':50},
      '4':{'vel':0.000002,'steps':10000000,'dcd':100000,'howmany':3,
                                                              'freq':50},
      '5':{'vel':0.0000002,'steps':100000000,'dcd':1000000,'howmany':1,
                                                             'freq':50}}
#______________________________________________________________________________
if len(sys.argv) >= 2:                               # load pickle if available
    confd=pickle.load(open(sys.argv[1],'rb'))
    mlist=confd['mlist']
    molec=confd['molec']
    ts=confd['ts']
    vels=confd['vels']
    x=confd['x']
    environ=confd['environ']
    zcrd=confd['zcrd']
    envdist=confd['envdist']
    gate=confd['gate']
    cn=confd['cn']
    comp=confd['comp']
    wallt=confd['wallt']
    queue=confd['queue']
    zdictn=confd['zdictn']
    zlabel=confd['zlabel']
    configf=confd['configf']
    selgate=confd['selgate']
    confign=confd['confign']
    configw=confd['configw']
    configq=confd['configq']
    confige=confd['confige']
    envdir=confd['envdir']
    strdir=confd['strdir']
    tstep=confd['tstep']
    dictpf=confd['dictpf']
    setup=confd['setup']
    langevD=confd['langevD']
#______________________________________________________________________________
def re_dist(script,mol,env,v):                             #regular expressions
    o=open(script,'r+')
    text=o.read()
    text=re.sub('xxstartconstraintxx',str(zdictn[envdist[env]]),text)
    econstraint=str((zdictn[envdist[env]])+(setup[v]['vel']*setup[v]['steps']))
    text=re.sub('xxendconstraintxx',econstraint,text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
def re_job(script,mol,env,v):
    o=open(script,'r+')
    text=o.read()
    bashjobname=mol+'.amb.'+str((setup[v]['vel'])*500000)+env.split('.')[1]
    text=re.sub('xxqueuexx',configq[queue],text)
    text=re.sub('xxjobnamexx',bashjobname,text)
    text=re.sub('xxnodesxx',confign[cn][comp],text)
    text=re.sub('xxwalltimexx',configw[wallt],text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
def re_npy(script,mol,env,v):
    o=open(script,'r+')
    text=o.read()
    num='0'+v
    text=re.sub('xxnumxx',num,text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
def re_expavg(script,mol,env,v):
    o=open(script,'r+')
    text=o.read()
    tefdir='0'+v+'.*/*-tef.dat*'
    num='0'+v
    text=re.sub('xxtefdirxx',tefdir,text)
    text=re.sub('xxnumxx',num,text)
    text=re.sub('xxvvxx',v,text)
    velaps=str((setup[v]['vel'])*500)
    text=re.sub('xxvelapsxx',velaps,text)
    velans=str((setup[v]['vel'])*500000)
    text=re.sub('xxvelansxx',velans,text)
    plotn1=mol+'amb'+env.split('.')[1]+str(confige[v])
    plotn2=str(zlabel[envdist[env]])
    plotname=plotn1+plotn2
    text=re.sub('xxplotnamexx',plotname,text)
    sconstraint=str(zdictn[envdist[env]])
    econstraint=str((zdictn[envdist[env]])+(setup[v]['vel']*setup[v]['steps']))
    text=re.sub('xxstartconstraintxx',sconstraint,text)
    text=re.sub('xxendconstraintxx',econstraint,text)
    text=re.sub('xxmoleculexx',mol,text)
    text=re.sub('xxenvironxx',env.split('.')[1],text)
    dt=str(((setup[v]['freq'])*(tstep[ts])/1000))
    text=re.sub('xxdtxx',dt,text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
def re_go(script,mol,env,v):
    dc=script.split('/')[-2]
    o=open(script,'r+')
    text=o.read()
    text=re.sub('xxhowmanyxx',str(setup[v]['howmany']),text)
    text=re.sub('xxstrucequilxx',str(strdir[env]),text)
    text=re.sub('xxnodecountxx',cn,text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
def re_smd(script,mol,env,v):
    dc=script.split('/')[-2]
    o=open(script,'r+')
    text=o.read()
    text=re.sub('xxstepsxx',str(setup[v]['steps']),text)
    text=re.sub('xxdcdxx',str(setup[v]['dcd']),text)
    text=re.sub('xxtsxx',str(tstep[ts]/1000),text)
    text=re.sub('xxfreqxx',str(setup[v]['freq']),text)
    text=re.sub('xxlDxx',langevD,text)
    o.close()
    o=open(script,'w+')
    o.write(text)
    o.close()
#_____________________________________________________________________________
def reg_exp(subdir,mol,env,v):                      # call regular expressions
    for root, dirnames, filenames, in os.walk(subdir):
        for fn in filenames:
            fn=os.path.join(root,fn)
            id=fn.split('/')[-1]
            if id=='job.sh':
                re_job(fn,mol,env,v)
            elif id=='go.py':
                re_go(fn,mol,env,v)
            elif id=='smd.in':
                re_smd(fn,mol,env,v)
            elif id=='dist.RST':
                re_dist(fn,mol,env,v)
            elif id=='expavg.py':
                re_expavg(fn,mol,env,v)
            elif id=='dualplot.py':
                re_expavg(fn,mol,env,v)
            elif id=='npy.py':
                re_npy(fn,mol,env,v)
#________________________________________________________________________
def copy_folder(subdir):                     # replicate in accord x dict
    ename=subdir+'/expavg.py'
    eloc=('/').join(subdir.split('/')[:-1])
    num=subdir.split('/')[-1]
    elocn=eloc+'/0'+num+'-expavg.py'
    os.system('mv %s %s' % (ename,elocn))
    npyname=subdir+'/npy.py'
    nloc=('/').join(subdir.split('/')[:-1])
    nlocn=nloc+'/0'+num+'-npy.py'
    os.system('mv %s %s' % (npyname,nlocn))
    dualname=subdir+'/dualplot.py'
    dloc=('/').join(subdir.split('/')[:-1])
    dlocn=dloc+'/0'+num+'-dualplot.py'
    os.system('mv %s %s' % (dualname,dlocn))
    folder=subdir.split('/')[-1]
    copies=x[folder]
    for f in range(0,copies+1):
        if f<10:
            fname=('/').join(subdir.split('/')[:-1])+'/'+ \
                   '0'+str(subdir.split('/')[-1])+'.0'+str(f)
        elif f>=10:
            fname=('/').join(subdir.split('/')[:-1])+'/'+ \
                  '0'+str(subdir.split('/')[-1])+'.'+str(f)
        shutil.copytree(subdir,fname)
#________________________________________________________________________
def make_folder(mol,env,zcrd):                        # make 5 velocities
    for v in vels:
        subdir=os.path.join(jobdir,env,v)
        sourcedir=os.path.join('0000-maindir',mol,envdir[env])
        shutil.copytree(sourcedir,subdir)
        jobfiles=os.path.join(maindir,selgate[gate]['job'])
        jobfiled=os.path.join(subdir,'job.sh')
        shutil.copy2(jobfiles,jobfiled)
        gofiles=os.path.join(maindir,selgate[gate]['go'])
        gofiled=os.path.join(subdir,'go.py')
        shutil.copy2(gofiles,gofiled)
        expfiles=os.path.join(maindir,'expavg-t.py')
        expfiled=os.path.join(subdir,'expavg.py')
        shutil.copy2(expfiles,expfiled)
        expfiles=os.path.join(maindir,'npy-t.py')
        expfiled=os.path.join(subdir,'npy.py')
        shutil.copy2(expfiles,expfiled)
        expfiles=os.path.join(maindir,'dualplot-t.py')
        expfiled=os.path.join(subdir,'dualplot.py')
        shutil.copy2(expfiles,expfiled)
        stfiles=os.path.join(maindir,mol,'dist.RST')
        stfiled=os.path.join(subdir,'dist.RST')
        shutil.copy2(stfiles,stfiled)
        reg_exp(subdir,mol,env,v)
        copy_folder(subdir)
        os.system('rm -r %s' % subdir)
#________________________________________________________________________
workdir=os.path.dirname(__file__)                     # working Directory
maindir=os.path.join(workdir,'0000-maindir')

for mol in molec:
    jobdirname=crdir+mol+'.'+str(zlabel[zcrd])
    jobdir=os.path.join(workdir,jobdirname)
    for env in environ:
        make_folder(mol,env,zcrd)
        strdir1=os.path.join(workdir,'08.struc-equil',mol,strdir[env])
        strdir2=os.path.join(jobdir,strdir[env])
        shutil.copytree(strdir1,strdir2)
    run=os.path.join(workdir,'pyscript/run.py')
    rund=os.path.join(jobdir,'run.py')
    shutil.copy(run,rund)
    pysc=os.path.join(workdir,'pyscript')
    pysd=os.path.join(jobdir,'pyscript')
    shutil.copytree(pysc,pysd)
    run=os.path.join(workdir,'pyscript/exprun.py')
    rund=os.path.join(jobdir,'exprun.py')
    shutil.copy(run,rund)
    dels=os.path.join(workdir,'pyscript/del.py')
    deld=os.path.join(jobdir,'del.py')
    shutil.copy(dels,deld)
#________________________________________________________________________
confd={}                                                       # a pickle
confd['mlist']=mlist
confd['molec']=molec
confd['ts']=ts
confd['vels']=vels
confd['x']=x
confd['environ']=environ
confd['zcrd']=zcrd
confd['envdist']=envdist
confd['gate']=gate
confd['cn']=cn
confd['comp']=comp
confd['wallt']=wallt
confd['queue']=queue
confd['zdictn']=zdictn
confd['zlabel']=zlabel
confd['configf']=configf
confd['selgate']=selgate
confd['confign']=confign
confd['configw']=configw
confd['configq']=configq
confd['confige']=confige
confd['envdir']=envdir
confd['strdir']=strdir
confd['tstep']=tstep
confd['dictpf']=dictpf
confd['setup']=setup
confd['langevD']=langevD
os.chdir(jobdir)
pickle.dump(confd,open('setup.pkl','w'))
