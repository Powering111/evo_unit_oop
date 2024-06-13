import uuid
import os

SEED = 31415

TMP_DIR = '/tmp/oop_test_gen'
TARGET_FILENAME = 'target.py'
TEST_FILENAME = 'test_target.py'

# defines if mutation is considered (extremely slower) and the weight of mutation to coverage
# mutation alpha of 1 means equal contribution to coverage, 2 means twice emphasis on mutation, and so on
MUTATION_ALPHA = 0

# defines if reciprocal of length (in thousand characters) will be used
# alpha of 1 means "equal" contribution to coverage, 2 means twice emphasis on rep_length, and so on
# reciprocal defined as min(1, 1000/length)
REC_LENGTH_ALPHA = 0 # 0.05

LENGTH_ALPHA = 0.05

USE_PYTEST = False

####################################################################

# Need this name to be pretty weird so that it does not occuring in the user code coincidentally
# Plus, random so that if the marginal chance does happen, it (most likely) not happening again in the next run
# Actually the code are from the evo team, so it is quite safe to assume the code are safe and just use some word, we can change this!
LOGGER_NAME = "log_" + str(uuid.uuid4().hex)[:5]
ASSERT_STR = "assert_" + str(uuid.uuid4().hex)[:5]
STRINGIFY_NAME = "strfy_" + str(uuid.uuid4().hex)[:5]

DO_MUTATION_TESTING = MUTATION_ALPHA != 0
DO_REC_LENGTH = REC_LENGTH_ALPHA != 0
DO_LENGTH = LENGTH_ALPHA != 0

# if we do mutation testing, we have to use pytest.
USE_PYTEST |= DO_MUTATION_TESTING

TARGET_PATH = os.path.join(TMP_DIR, TARGET_FILENAME)
TEST_PATH = os.path.join(TMP_DIR, TEST_FILENAME)

