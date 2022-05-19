This script will attempt to reverse engineer an equation which matches data provided to it. 
I am currently feeding in data which would match SUVAT equations which i hope to reverse engineer from the data alone.
this is technically a form of recurrent neueral network, a large sample of random equations are created (1 per neuron), then each of these equations are tested for error against the data. 
The neuron with best rmse is choosen as the parent for the next generation of nerons. each of the next generation of neurons are a small iteration upon their parent. 
the best neuron is then chosen again and is the basis for the next generation. 
i have included a file which is an example of sample output. i find excel files are the best way to watch the equations change over time however be carful about accidently creating 1000's of files.
