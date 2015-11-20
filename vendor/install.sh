PYTHON_LIBS=`ls */setup.py`

for PYTHON_LIB in $PYTHON_LIBS
do
	pushd `dirname $PYTHON_LIB`
	python setup.py install
	popd
done
