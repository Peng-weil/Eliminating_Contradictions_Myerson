# Eliminating Logical Contradictions based on the Myerson Value

The code for `Eliminating Logical Contradictions based on the Myerson Value`, we used the datasets provided by the following repositories, including the ontology's OWL file with the MUPS file, with sincere thanks.
```
1. Embedding-based Approach to Repairing Incoherent Ontologies. (https://github.com/QiuJi345/embRepair)
2. A Benchmark for Incoherent Ontologies. (https://github.com/QiuJi345/IncOntologyBenchmark)
3. Resolving Logical Contradictions in Description Logic Ontologies Based on Integer Linear Programming(https://github.com/qiuji123/ilpConflicts)
```



## Project structure

```.
├── data
│   ├── mups
│   └── owl
├── draw
├── log
│   └── all.log
└── fig_visual.py
└── ontology_graph_visualization.py
└── ontology_myerson.py
```
`mups`: store the mups file of the ontology. Please name the downloaded mups file as `res.txt` and place it under the corresponding ontology folder, at the same level as the `Readme` in it.

`owl`: store the owl file of the ontology. Please place the downloaded owl file in this folder, at the same level as the `Readme` in it.

`ontology_myerson.py`: This file is used to reproduce the experimental results in the paper.


## Project environment

Please refer to `environment.yaml` for the environment dependencies.

To solve linear programming models, it is necessary to install CPLEX 20.1.0 from https://www.ibm.com/products/ilog-cplex-optimization-studio/cplex-optimizer.  
The academic version is available at https://community.ibm.com/community/user/ai-datascience/blogs/xavier-nodet1/2020/07/09/cplex-free-for-students.

## Run the code

To reproduce the experimental results in the paper, run the following command:

```
python ontology_myerson.py --ontology ontology --density 0.15 --nx_seed 30
```

"ontology_graph_visualization.py" can be used to generate the visualization of all ontologies, with the same usage as "ontology_myerson.py".

This command will run all ontology files in bulk. Additionally, generating a graph for ontology km1500_i500-3500 is time consuming, so you could also choose to replace the parameter "ontology" with the name of a single ontology to execute the command. Furthermore, "--nx_seed 30" indicates that the command will sequentially use 30 random seeds to generate the graph for the ontology.
