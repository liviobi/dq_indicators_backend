import os
from subprocess import check_output
from config import cfg


path = os.path.abspath(os.path.join(cfg["uploadDir"], "prose.txt"))

result = check_output(
    ['java', '-jar', './java-indicators/java-indicators.jar', path])
print(result.decode().split(","))
