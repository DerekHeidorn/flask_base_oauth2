
from project.app.persist import codetableDao

def getCodeTable(codetableName):

    codetableData = codetableDao.getCodeTable(codetableName)

    return codetableData