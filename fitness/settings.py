import uuid
# Need this name to be pretty weird so that it does not occuring in the user code coincidentally
# Plus, random so that if the marginal chance does happen, it (most likely) not happening again in the next run
# Actually the code are from the evo team, so it is quite safe to assume the code are safe and just use some word, we can change this!
LOGGER_NAME = "log_" + str(uuid.uuid4().hex)[:5]
ASSERT_STR = "assert_" + str(uuid.uuid4().hex)[:5]

TMP_DIR = '/tmp/oop_test_gen'
TARGET_FILENAME = '/tmp/oop_test_gen/target.py'
TEST_FILENAME = '/tmp/oop_test_gen/test_target.py'
