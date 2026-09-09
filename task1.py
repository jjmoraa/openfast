import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
try:
    from welib.tools.figure import *
except:
    pass

from helper_functions import *

# Welib
import welib.weio as weio
from welib.tools.stats import mean_rel_err


export=True

IPlot=[]
IPlot+=[0]# Postprocessing
IPlot+=[1] # plotting

def store_lines(folder='task1_uniform_aligned', U0=12, zMid=250, filebases=None, DPlanes=None, D=126, outDir='_data/'):
    # Default values
    if filebases is None:
        filebases= { 'cart': 'input_cart' }
    if DPlanes is None:
        DPlanes = [1, 5, 8]
    
    case = os.path.basename(folder)

    # Look at max index for first file. Assume consistency betweeen files
    filebase1 = filebases[list(filebases.keys())[0]]
    Indices, iMax, n = vtkIndices(folder, '{}.Low.DisYZ'.format(filebase1))
    print('iMax', iMax)

    # Output dictionary
    outDict = {}
    outDict['U0'] = U0
    outDict['D'] = D
    outDict['DPlanes'] = DPlanes
    outDict['iMax'] = iMax
    outDict['labels']  = list(filebases.keys())

    # Storing outDict[label][Dplane]
    for ilab, (label, filebase) in enumerate(filebases.items()):
        df = weio.read(os.path.join(folder, filebase+'.T1.out')).toDataFrame()
        CT = df['RtAeroCt_[-]'].mean()
        print(f'{label:10s}: CT={CT:.3f}')
        outDict[label] = {}
        # --- Extract Planes and Lines for each downstream position
        for iPlane, Dplane in enumerate(outDict['DPlanes']):
            Y, Z, Ux, _, _ = extractPlane('YZ', folder, filebase, iPlane=iPlane+1, iTime=iMax, removeBoundaries=None, U0=U0, D=D, n=n)
            y, Uh, z, Uv = extractLines(Y, Z, 0, zMid/D, Ux)
            if ilab==0:
                outDict['y'] = y
                outDict['z'] = z
            outDict[label][Dplane] = {'Ux':Ux, 'Uh':Uh, 'Uv':Uv}
    # Dump to file
    outFile = os.path.join(outDir, case + '.pkl')
    print('>>> outFile', outFile)
    save_dict(outFile, outDict)


def plotWakeDef(ax, dy, UDict, title='', ylim=[-1.5,1.4], xlim=[.45,1.1]):
    for label, Uh in UDict.items():
        if label=='Curl':
            ax.plot(Uh, dy, '-o', c=cCurl, label=label, ms=4)
        elif label=='Polar':
            ax.plot(Uh, dy, '--', c=cPolr, label=label)
        elif label=='Cartesian':
            ax.plot(Uh, dy, '--', c=cCart, label=label)
        else:
            ax.plot(Uh, dy, '-', label=label)
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    ax.set_xlabel(r'$u/U_\infty$')
    ax.grid(True, linestyle=':', color=(0.5,0.5,0.5))
    ax.set_title(title)
    ax.tick_params(direction='in', top=True, right=True, which='both')
    if iPlane==1:
        ax.legend(loc='upper left')
        ax.set_ylabel(r'$y/D$')


# --------------------------------------------------------------------------------}
# --- PostPro
# --------------------------------------------------------------------------------{
outDir='_data/'
filebases = {
    #'Curl'     :'input_curl',
    #'Polar'    :'input_polar',
    #'Cartesian':'input_cart',
    'Polar_new'    :'input_polar_new',
    'Curl_new'     :'input_curl_new',
    'Cart_new':'input_cart_new',
    }

if 0 in IPlot:
    store_lines(folder='task1_uniform_aligned', U0=12, zMid=250, filebases=filebases, D=126, outDir=outDir)

if 1 in IPlot:
    d = load_dict('_data/task1_uniform_aligned.pkl')

    fig,axes = plt.subplots(1, 3, sharey=True, figsize=(12.8,3.8)) # (6.4,4.8)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.930, bottom=0.133, hspace=0.20, wspace=0.14)
    for iPlane,Dplane in enumerate(d['DPlanes']):
        UDict = {}
        for label in d['labels']:
            UDict[label] = d[label][Dplane]['Uh']
        ax=axes[iPlane]
        plotWakeDef(ax, d['y'], UDict, title='{}D'.format(Dplane), ylim=[-1.5,1.5])
        eps = mean_rel_err(y1=UDict['Polar_new'][5:-5], y2=UDict['Curl_new'][5:-5], method='loc', verbose=True, varname='Ux')
        ax.text(0.90,1.270,r'$\epsilon={:.1f}$%'.format(eps), fontsize=14, ha='center')
    fig._title='Task1Deficit'
    plt.show()
    
if export:
    setFigurePath('../article/figs/')
    export2pdf()
plt.show()
