#!/bin/sh
abspath=$(cd "$(dirname "$0")"; pwd)
CLASSPATH=$CLASSPATH:$abspath/"lib/*":$abspath/"bin"
export CLASSPATH
java -classpath $CLASSPATH edu.mit.csail.PaperRecommender $abspath/../../data/chi2013/data_lenskit.txt $abspath/../../data/chi2013/data_lenskit_user.txt