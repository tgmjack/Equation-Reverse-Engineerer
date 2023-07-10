This script will attempt to reverse engineer an equation from data provided to it. 

The data at the top of the code, which I am currently feeding in, would match SUVAT equations which i hope to reverse engineer from the data alone.

this is technically a form of genetic algorythm, a large sample of random equations are created (1 equation per neuron), then each of these equations are tested for error against the data.

The neuron with best rmse is choosen as the parent for the next generation of neurons. each of the next generations neurons are a small change upon their parent. 
the best neuron is then chosen again and is the basis for the next generation. 

### if you get a file outpted with "jesus it worked" in the title, then that equation both has a very low rmse and correctly predicts a variable from unseen data (so its probably correct)





##########################

Technically this project has proven impossible since there are an infinite number of arbitrary equations to match any dataset .... 

on one level technically it works. it does produce an equation that matches your data (see example csv)... however i put in suvat equations and it is impossible to reverse engineer an equation that will predict unseen data due to the infinite number of potential solutions

I tried using a regularizer to punish it for too many terms but its hard to cut down on infinite. 
