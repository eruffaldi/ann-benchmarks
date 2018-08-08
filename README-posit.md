SYSTEM is Python 3.6

python run.py --definitions algos_po.yaml --dataset glove-100-angular
python run.py --help
python plot.py --dataset glove-100-angular

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