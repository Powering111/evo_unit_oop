import os 

def write_target (target_code: str, test_suite: str) : 
    os.chdir('/tmp')
    with open ('target.py', 'w') as f: 
        f.write(target_code) 
    with open('test_target.py', 'w') as f:
        f.write(test_suite)
