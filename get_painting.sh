#/bin/bash
# Paint forever 
#   Select random subject and artist
#   Create images
#   Upload
#   Tweet about it (e.g. @visplastica)
while true
do
	rm output/*
	PROMPT="`shuf -n1 subjects.txt` by `shuf -n1 artists.txt`"
	BASENAME=`sed 's/ /_/g' <<< "$PROMPT"`
	echo Prompt $PROMPT
	#echo BASENAME $BASENAME  
	python clip_draw.py -p "$PROMPT" -f "$BASENAME" -i 500
	./display_image_on_terminal.sh "done/${BASENAME}_x4.png"
	python upload.py -f "$BASENAME"
        python tweeter.py -t "${PROMPT}." -f "done/${BASENAME}_x2.png"
done
