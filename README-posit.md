
# For local testing use
export PYTHONPATH=../posit_kdtree/build/python

# Minimal docker build
	docker images | grep ann-benchmarks
	docker rmi ann-benchmarks-positkdd
	python3 install.py --algorithm flann
	python3 install.py --algorithm positkdd --build-arg gituser=... gitpass=...
	
## Login 

	docker run --rm -ti --entrypoint "" ann-benchmarks-positkdd bash

## Types info
	 python3 posit_kdtree/python/nanoflann_any.py --info

# Then
python run.py --definitions algos_po.yaml --local --dataset fashion-mnist-784-euclidean

MAYBE python plot.py --dataset fashion-mnist-784-euclidean --definitions algos_po.yaml

## can run without docker!
	--local
## can run single algorithm
	--algorithm


# Examples

 python run.py --list-algorithms --definitions algos_po.yaml

# Installation Test local

 export PYTHONPATH=../posit_kdtree/build/python
 python -m ann_benchmarks.algorithms.positkdd

# Issues

- posit timing suffers float conversion so in theory we should support a phase of converting the input, at least for building

- angular metric is not supported due to lack of implementation in our nanoflann
	Angular Metric is special because it is 1-ab/||a||^2 ||b||^ 

	The accumulation formulation of the cosine metric has to be clarified

- hamming metric is present 