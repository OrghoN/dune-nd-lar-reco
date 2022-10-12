#GLOBUS file transfer protocol tutorial
Oct. 12, 2022
Orgho Neogi<anoronyo@gmail.com>




















{::comment}

#Slac endpoint
dda770be-f428-11eb-ab64-d195c983855c
#SLAC FilePath
/gpfs/slac/staas/fs1/g/neutrino/anoronyo/globusTest.txt
#SLAC Combined
dda770be-f428-11eb-ab64-d195c983855c:/gpfs/slac/staas/fs1/g/neutrino/anoronyo/globusTest.txt

#WC Endpoint
b251fb72-0f23-11eb-abe1-0213fe609573
#WC FilePath
/work1/dune/users/oneogi/globusTest.txt
#WC Combined
b251fb72-0f23-11eb-abe1-0213fe609573:/work1/dune/users/oneogi/globusTest.txt

#Transfer Command Test
globus transfer b251fb72-0f23-11eb-abe1-0213fe609573:/work1/dune/users/oneogi/globusTest.txt dda770be-f428-11eb-ab64-d195c983855c:/gpfs/slac/staas/fs1/g/neutrino/anoronyo/globusTest.txt

# Globus large file test 1.8 G
globus transfer b251fb72-0f23-11eb-abe1-0213fe609573:/wclustre/dune/jwolcott/dune/nd/nd-lar-reco/supera/singles/neutrino.0.larcv.root dda770be-f428-11eb-ab64-d195c983855c:/gpfs/slac/staas/fs1/g/neutrino/anoronyo/globusTest.root

#large file details
globus task show e4a9d764-4a7e-11ed-b802-855d8beae885
{:/comment}