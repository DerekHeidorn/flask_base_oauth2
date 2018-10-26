
from persist import codetableDao

def geCodeTable(codetableName):

    codetableData = codetableDao.getCodeTable(codetableName)

    return codetableData