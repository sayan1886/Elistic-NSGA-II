from dataclasses import dataclass
from os.path import dirname, realpath
from typing import Any
import json
    
@dataclass
class Crossover:
    crossover_probability: float
    crossover_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Crossover':
        _crossover_probability = float(obj.get("crossover_probability")) \
                    if obj.get("crossover_probability") is not None else 0.6
        _crossover_type = str(obj.get("crossover_type")) \
                    if obj.get("crossover_type") is not None else "single"
        return Crossover(crossover_probability=_crossover_probability,
                         crossover_type=_crossover_type)
    
@dataclass
class Mutation:
    mutation_probability: float
    mutation_type: str
    participant_bits: int

    @staticmethod
    def from_dict(obj: Any) -> 'Mutation':
        _mutation_type = str(obj.get("mutation_type")) \
                    if obj.get("mutation_type") is not None else "bit-flip"
        _participant_bits = int(obj.get("participant_bits")) \
                    if obj.get("participant_bits") is not None else 2
        _mutation_probability = float(obj.get("mutation_probability")) \
                    if obj.get("mutation_probability") is not None else 0.1
        return Mutation(mutation_type=_mutation_type, 
                        participant_bits=_participant_bits,
                        mutation_probability=_mutation_probability)
        
@dataclass
class Objective:
    num_of_objective: int
    objective_type: str
    expand : bool

    @staticmethod
    def from_dict(obj: Any) -> 'Objective':
        _num_of_objective = int(obj.get("num_of_objective")) \
                if obj.get("num_of_objective") is not None else 1
        _objective_type = str(obj.get("objective_type")) \
                if obj.get("objective_type") is not None else "min"
        _expand = bool(obj.get("expand")) if obj.get("expand") is not None else True
        return Objective(num_of_objective=_num_of_objective, 
                         objective_type=_objective_type, 
                         expand=_expand)
        
@dataclass
class Range:
    min: float
    max: float
    variable_range: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Range':
        _min = float(obj.get("min")) if obj.get("min") is not None else 0
        _max = float(obj.get("max")) if obj.get("max") is not None else 0
        _variable_range = _min != _max
        return Range(min=_min, max=_max, variable_range=_variable_range)
    
@dataclass
class Selection:
    selection_type: str
    participants: int
    tournament_probability: float

    @staticmethod
    def from_dict(obj: Any) -> 'Selection':
        _selection_type = str(obj.get("selection_type"))\
                    if obj.get("selection_type") is not None else "tournament"
        _participants = int(obj.get("participants")) \
                    if obj.get("participants") is not None else 2
        _tournament_probability = float(obj.get("tournament_probability")) \
                    if obj.get("tournament_probability") is not None else 1.0
        return Selection(selection_type=_selection_type, 
                         participants=_participants,
                         tournament_probability=_tournament_probability )

@dataclass 
class Config:
    crossover: Crossover
    mutation: Mutation
    objective: Objective
    range: Range
    selection: Selection
    num_of_chromosomes: int
    num_of_gene: int
    num_of_generations: int
    num_of_individuals: int
    plot_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        _crossover = Crossover.from_dict(obj.get("crossover"))
        _mutation = Mutation.from_dict(obj.get("mutation"))
        _objective = Objective.from_dict(obj.get("objective"))
        _range = Range.from_dict(obj.get("range"))
        _selection = Selection.from_dict(obj.get("selection"))
        _num_of_chromosomes = int(obj.get("num_of_chromosomes"))
        _num_of_gene =  int(obj.get("num_of_gene"))
        _num_of_generations = int(obj.get("num_of_generations"))
        _num_of_individuals = int(obj.get("num_of_individuals"))
        _plot_type = str(obj.get("plot_type"))
    
        return Config(crossover=_crossover, mutation=_mutation, 
                        objective=_objective, range=_range,
                        selection=_selection, 
                        num_of_chromosomes=_num_of_chromosomes,
                        num_of_gene=_num_of_gene, 
                        num_of_generations=_num_of_generations,
                        num_of_individuals=_num_of_individuals,
                        plot_type=_plot_type)   
    
    
def __get_config_file_name(exampleDirName):
    # print("Multi-Objective Genetic Algorithm Config Selection:")
    # print("1. Binary Tournament Selection with Bit Flip Mutation")
    # print("2. Binary Tournament Selection with Bit Swap Mutation")
    # print("3. Roulette-Wheel Selection with Bit Flip Mutation")
    # print("4. Roulette-Wheel Selection with Bit Swap Mutation")
    # option = input("Enter your choice: ")
    option = 1
    root_dir = dirname(realpath(__file__))
    file_name = ""
    selected_option = "Binary Tournament Selection with Bit Flip Mutation"
    if option == "1":
        file_name = root_dir + "/" + exampleDirName + "/bts_bit_flip.json"
        selected_option = "Binary Tournament Selection with Bit Flip Mutation"
    elif option == "2":
        file_name = root_dir + "/" + exampleDirName + "/bts_bit_swap.json"
        selected_option = "Binary Tournament Selection with Bit Swap Mutation"
    elif option == "3":
        file_name = root_dir + "/" + exampleDirName + "/roulette_bit_flip.json"
        selected_option = "Roulette-Wheel Selection with Bit Flip Mutation"
    elif option == "4":
        file_name = root_dir + "/" + exampleDirName + "/roulette_bit_swap.json"
        selected_option = "Roulette-Wheel Selection with Bit Swap Mutation"
    else:
        file_name = root_dir + "/" + exampleDirName + "/bts_bit_flip.json"
        selected_option = "Binary Tournament Selection with Bit Flip Mutation"
    return file_name, selected_option    

def get_config(exampleName)->Config:
    config_file_name, selected_option = __get_config_file_name(exampleName)
    with open(config_file_name,'r') as file:
        configString = file.read()
        
    configJSON = json.loads(configString)
    config = Config.from_dict(configJSON)
    return config