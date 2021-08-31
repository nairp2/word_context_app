# word_context_app

# a python script that provides the context of the input word in multiple word documents, the directory name and path it exists within. Text indexing is performed if the words exist and a heatmap is displayed.



I would suggest making a new virtual environment in anaconda. Type the following in the anaconda terminal

conda install -c conda-forge spacy 

python -m spacy download en_core_web_lg

conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge

conda install -c huggingface transformers

conda install -c conda-forge sentence-transformers



Afterwards the script should be good to run
