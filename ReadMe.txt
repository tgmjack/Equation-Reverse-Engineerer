This script will attempt to reverse engineer an equation from data provided to it. 

The data at the top I am currently feeding in data which would match SUVAT equations which i hope to reverse engineer from the data alone.

this is technically a form of genetic algorythm, a large sample of random equations are created (1 equation per neuron), then each of these equations are tested for error against the data.

The neuron with best rmse is choosen as the parent for the next generation of nerons. each of the next generations neurons are a small change upon their parent. 
the best neuron is then chosen again and is the basis for the next generation. 

### if you get a file outpted with "jesus it worked" in the title, then that equation both has a very low rmse and correctly predicts a variable from unseen data (so its probably correct)





##########################

Technically this project has proven impossible since there are an infinite number of arbitrary equations to match any dataset .... However the only good rmse's i seem to calculate involve huge numbers of terms or polynomial/indices with a ridiculous nu,ber of decimals.   im currently experimenting with regularizers to see if that can be cut out unwanted solutions...  
