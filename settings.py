import numpy as np

TITLE = "Boat AI"
CAMERA_SIZE = (800, 900)
PATH_BOAT = "images/boat_img.png"
PATH_RIVER = "images/river1.png"
PATH_ICON = "images/boat_icon.png"
PATH_X = "images/X.png"
COLOR_RIVER = (121, 191, 255)
FPS = 30

BOAT_INITIAL_POSITION = (320, 730)
BOAT_SCALE = (120, 45)

RIVER_SCALE = (800, 1800)
X_SCALE = (10, 10)

MASS = 1000
LENGTH = 0.00005
K = 0.5
FORCE_LIMIT = 1

WIDTH = 800
HEIGHT = 1800

MAX_VISION_DISTANCE = 300
NUM_PLAYER = 3

SAVE_PATH = "gen_save"
LOAD_PATH = None

TIME_MAX = 10
END_GENERATION = 1

GA_SETTINGS = {

    #### GA stuff ####

    ## Mutation ##

    # Mutation rate is the probability that a given gene in a chromosome will randomly mutate
    'mutation_rate': 0.05,  # Value must be between [0.00, 1.00)
    # If the mutation rate type is static, then the mutation rate will always be `mutation_rate`,
    # otherwise if it is decaying it will decrease as the number of generations increase
    'mutation_rate_type': 'static',  # Options are [static, decaying]
    # The probability that if a mutation occurs, it is gaussian
    'probability_gaussian': 1.0,  # Values must be between [0.00, 1.00]
    # The probability that if a mutation occurs, it is random uniform
    'probability_random_uniform': 0.0,  # Values must be between [0.00, 1.00]

    ## Crossover ##

    # eta related to SBX. Larger values create a distribution closer around the parents while smaller values venture further from them.
    # Only used if probability_SBX > 0.00
    'SBX_eta': 100,
    # Probability that when crossover occurs, it is simulated binary crossover
    'probability_SBX': 0.5,
    # The type of SPBX to consider. If it is 'r' then it flattens a 2D array in row major ordering.
    # If SPBX_type is 'c' then it flattens a 2D array in column major ordering.
    'SPBX_type': 'r',  # Options are 'r' for row or 'c' for column
    # Probability that when crossover occurs, it is single point binary crossover
    'probability_SPBX': 0.5,
    # Crossover selection type determines the way in which we select individuals for crossover
    'crossover_selection_type': 'roulette_wheel',

    ## Selection ##

    # Number of parents that will be used for reproducing
    'num_parents': 10,
    # Number of offspring that will be created. Keep num_offspring >= num_parents
    'num_offspring': 20,
    # The selection type to use for the next generation.
    # If selection_type == 'plus':
    #     Then the top num_parents will be chosen from (num_offspring + num_parents)
    # If selection_type == 'comma':
    #     Then the top num_parents will be chosen from (num_offspring)
    # @NOTE: if the lifespan of the individual is 1, then it cannot be selected for the next generation
    # If enough indivduals are unable to be selected for the next generation, new random ones will take their place.
    # @NOTE: If selection_type == 'comma' then lifespan is ignored.
    #   This is equivalent to lifespan = 1 in this case since the parents never make it to the new generation.
    'selection_type': 'plus',  # Options are ['plus', 'comma']

    ## Individual ##

    # How long an individual is allowed to be in the population before dying off.
    # This can be useful for allowing exploration. Imagine a top individual constantly being selected for crossover.
    # With a lifespan, after a number of generations, the individual will not be selected to participate in future
    # generations. This can allow for other individuals to have higher selective pressure than they previously did.
    # @NOTE this only matters if 'selecton_type' == 'plus'. If 'selection_type' == 'comma', then 'lifespan' is completely ignored.
    'lifespan': np.inf,  # Options are any positive integer or np.inf (typed out as if it were a number, i.e. no quotes to make it a string)
    # The type of vision the snake has when it sees itself or the apple.
    # If the vision is binary, then the input into the Neural Network is 1 (can see) or 0 (cannot see).
    # If the vision is distance, then the input into the Neural Network is 1.0/distance.
    # 1.0/distance is used to keep values capped at 1.0 as a max.
}