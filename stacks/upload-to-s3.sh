#!/bin/bash

while getopts ":p:" opt; do
	case ${opt} in
		p )
			filename=$OPTARG;
		;;
		\? )
			echo "Invalid Option: -$OPTARG" 1>&2
			usage;
		;;
		: )
			echo "Invalid Option: -$OPTARG requires an argument" 1>&2
			usage;
		;;
		 * )
			echo "Unimplemented option" 1>&2
			usage;
		;;
	esac
done

aws s3 sync ../build/distributions s3://sharedbucketsintyaegarboo-s3bucketsharedresources-boencsukew48/code/lambda --exclude "*" --include ${filename}