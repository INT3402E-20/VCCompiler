import glob
import subprocess
import os

if not os.path.exists('./out'):
    os.makedirs('./out')

filenames = []
for f in glob.glob('./tests/*.vc'):
    filename = './out/' + f.rsplit('/', maxsplit=1)[1] + 'tok'
    process = subprocess.run(
        ['vclexer', f, '-o', filename], stdout=subprocess.PIPE)
    filename = './out/' + f.rsplit('/', maxsplit=1)[1] + 'tok'
    filenames.append(filename)

diff_file = open('./diff.txt', 'w')
for f in filenames:
    mine = f
    sol = 'tests/' + f
    diff_file.write("testing " + mine + "  and  " + sol)
    diff_file.write("--------------------------------------------")
    cp = subprocess.run(['diff', mine, sol], stdout=subprocess.PIPE)
    output = cp.stdout
    diff_file.write(output.decode('utf-8'))
    diff_file.write("--------------------------------------------\n\n")


diff_file.close()
