#!/bin/bash

if [[ -z $1 ]]; then
	echo "Need to specify folder!"
	exit 1
fi

mkdir ${1}wav
for sfile in midi_files/soundfonts/*.sf2
do
	dir=${1}wav/${sfile##*/}
	dir=${dir%.*}
	mkdir $dir
	touch ${dir}/files.txt
	for file in $1*.mid
	do
		ofile=${file/%mid/wav}
		ofile=${ofile##*/}
		FluidSynth/fluidsynth -F ${dir}/${ofile} -i -n -T wav $sfile $file
		echo "$ofile" >> ${dir}/files.txt
	done
done