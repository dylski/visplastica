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
		#rm ${OUTPUT}/*
		PROMPT="ballet dancers in the street by Degas"
		BASENAME=`sed 's/ /_/g' <<< "$PROMPT"`
		OUTPUT="${OUTPUT_BASE}_${BASENAME}_${TODAY}_$(date +%H_%M)"
		LOCALNAME="${OUTPUT}/highres_final_tiled_image_0.png"
		OUTPUT_NAME="${BASENAME}_${TODAY}_$(date +%H_%M).png"
		echo Prompt $PROMPT
		#echo BASENAME $BASENAME  
		echo Run Arheim --prompt ${PROMPT} --num_patches=${num_patches} --no-gui
		echo Output will go to ${OUTPUT}

		echo python arnheim/arnheim_3/main.py --config arnheim/arnheim_3/configs/jnano.yaml --output_dir "$OUTPUT" --global_prompt "${PROMPT}"
		python arnheim/arnheim_3/main.py --config arnheim/arnheim_3/configs/jnano.yaml --output_dir "$OUTPUT" --global_prompt "${PROMPT}"

		echo cp "$LOCALNAME" done/display.png
		cp "$LOCALNAME" done/display.png

		echo scp "$LOCALNAME" "dylski@xmasvibe.com:visplastica.com/gallery/${OUTPUT_NAME}"
		scp "$LOCALNAME" "dylski@xmasvibe.com:visplastica.com/gallery/${UNIQUE_FILENAME}"
		ssh dylski@xmasvibe.com 'rm visplastica.com/cached-index.html'
		# Use a copy so easy to reshow from command line if the terminal gets reset
		echo ./display_image_on_terminal.sh "${LOCALNAME}"
		./display_image_on_terminal.sh "${LOCALNAME}"
		echo python tweeter.py -t "${PROMPT}." -f "${LOCALNAME}"
		python tweeter.py -t "${PROMPT}." -f "${LOCALNAME}"
		echo python instapost.py -t "${PROMPT}." -u "${OUTPUT_NAME}"
		python instapost.py -t "${PROMPT}." -u "${UNIQUE_FILENAME}"
	done
	DATE=${TODAY}
done

