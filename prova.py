import os
from subprocess import check_output
from config import cfg


pathFile = os.path.abspath(os.path.join(cfg["uploadDir"], "prose.txt"))

pathModels = os.path.abspath("./java-indicators/models")

result = check_output(
    ['java', '-jar', './java-indicators/java-indicators.jar', pathFile, pathModels])
result = result.decode().split(",")[0][0:4]
print(type(result))
