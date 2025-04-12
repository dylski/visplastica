#/bin/bash
# Paint forever 
#   Select random subject and artist
#   Create images
#   Upload
#   Tweet about it (e.g. @visplastica)
OUTPUT_BASE="a3out"
DATE=99
for num_patches in 64
do
	TODAY=$(date +%Y_%m_%d)
	while true;  # [ $TODAY = $DATE ];
	do
		TODAY=$(date +%Y_%m_%d)
		#rm ${OUTPUT}/*
		PROMPT="a photograph of a face"
		BASENAME=`sed 's/ /_/g' <<< "$PROMPT"`
		OUTPUT="${OUTPUT_BASE}_${BASENAME}_${TODAY}_$(date +%H_%M)"
		LOCALNAME="${OUTPUT}/highres_final_tiled_image_0.png"
		OUTPUT_NAME="${BASENAME}_${TODAY}_$(date +%H_%M).png"
		echo Prompt $PROMPT
		#echo BASENAME $BASENAME  
		echo Run Arheim --prompt ${PROMPT} --num_patches=${num_patches} --no-gui
		echo Output will go to ${OUTPUT}

		#RED=$((RANDOM%128 + 64))
		#GREEN=$((RANDOM%128 + 64))
		#BLUE=$((RANDOM%128 + 64))
		RED=0
		GREEN=0
		BLUE=0
		echo python arnheim/arnheim_3/main.py --config arnheim/arnheim_3/configs/jnano.yaml --output_dir "$OUTPUT" --background_red $RED --background_green $GREEN --background_blue $BLUE
		# --global_prompt "${PROMPT}"
		python arnheim/arnheim_3/main.py --config arnheim/arnheim_3/configs/jnano.yaml --output_dir "$OUTPUT" --background_red $RED --background_green $GREEN --background_blue $BLUE
		# --global_prompt "${PROMPT}"

		echo cp "$LOCALNAME" "done/${OUTPUT_NAME}"
		cp "$LOCALNAME" "done/${OUTPUT_NAME}"
		convert "$LOCALNAME" -rotate 90 "done/display.png"

		echo scp "$LOCALNAME" "dylski@xmasvibe.com:visplastica.com/gallery/${OUTPUT_NAME}"
		scp "$LOCALNAME" "dylski@xmasvibe.com:visplastica.com/gallery/${OUTPUT_NAME}"
		scp "$LOCALNAME" "dylski@xmasvibe.com:visplastica.com/latest_display.png"
		ssh dylski@xmasvibe.com 'rm visplastica.com/cached-index.html'
		# Use a copy so easy to reshow from command line if the terminal gets reset
		echo ./display_image_on_terminal.sh "done/display.png"
		./display_image_on_terminal.sh "done/display.png"
		echo python tweeter.py -t "${PROMPT}." -f "${LOCALNAME}"
		python tweeter.py -t "${PROMPT}." -f "${LOCALNAME}"
		echo python instapost.py -t "${PROMPT}." -u "${OUTPUT_NAME}"
		python instapost.py -t "${PROMPT}." -u "${OUTPUT_NAME}"
	done
	DATE=${TODAY}
done

