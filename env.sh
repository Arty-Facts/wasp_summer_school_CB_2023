#! /bin/bash
__banner()
{
    echo "============================================================"
    echo $*
    echo "============================================================"
}

if [[ $1 == "clean" ]]; then 
    __banner Remove old env...
    if [[ -d "venv" ]]; then 
        rm -rf venv/ 
    fi
fi

python3 -m venv venv


__banner Instaling base packages... 
./venv/bin/pip install -e .


chmod +x venv/bin/activate

# start env
source ./venv/bin/activate
