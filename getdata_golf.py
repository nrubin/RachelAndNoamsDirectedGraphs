import urllib, urllister
from BeautifulSoup import BeautifulSoup
import csv

#------------General Use Functions-------------#
def getUrls(url):
    '''Returns a list of urls linked to from the given page'''
    sock = urllib.urlopen(url)
    parser = urllister.URLLister()
    parser.feed(sock.read())
    sock.close()
    parser.close()
    return parser

def getHTMLSource(url):
    '''Returns the HTML source code of the given page'''
    sock = urllib.urlopen(url)
    source = sock.read()
    sock.close()
    return source

def getPlayerName(playerStatsUrl):
    '''Returns the name of a player, given the URL of
    his stats page'''
    html = getHTMLSource(playerStatsUrl)
    soup = BeautifulSoup(''.join(html))
    line = soup.find('h1')
    name = line.renderContents()
    name = name.replace('  ', ' ')
    return name

def getMainTable(url):
    '''Finds the main table on a page of html and returns a list 
    of its rows, where each row is a comma-separated list of 
    columns' contents.'''
    html = getHTMLSource(url)
    soup = BeautifulSoup(''.join(html))
    table = soup.find('tbody')

    rows = table.findAll('tr')
    parsedTable = []
    for tr in rows:
        cols = tr.findAll('td')
        row = []
        for td in cols:
            text = td.renderContents()
            row.append(text)
        parsedTable.append(row)
    return parsedTable

#----------Specific Functions-------------------#
def getLastInitialUrls():
    source = "http://www.databasegolf.com/players/playerlist.htm"
    sock = urllib.urlopen(source)
    parser = urllister.URLLister()
    parser.feed(sock.read())
    sock.close()
    parser.close()
    
    lastinit = []
    for url in parser.urls:
        if "/players/playerlist.htm?lt=" in url:
            fullurl = "http://www.databasegolf.com" + url
            lastinit.append(fullurl)
    return lastinit

def getPlayerCareerURLS():
    '''Returns a list of players' stats pages'''
  
    lastInitials = getLastInitialUrls()
    playerspages = []
    for letter in lastInitials:
        parser = getUrls(letter)
        for url in parser.urls:
            if "playerpage.htm?samid" in url:
                 playerPage = "http://www.databasegolf.com/players/" + url
                 playerspages.append(playerPage)
    playerspages.remove('http://www.databasegolf.com/players/playerpage.htm?samid=GilbeGib02')
    playerspages.remove('http://www.databasegolf.com/players/playerpage.htm?samid=GilbeGib01')
    return playerspages

def getYear(yearUrl):
    ''' Year is given as a url. need to extract the year'''
    pieces = yearUrl.split('<')
    pieces = pieces[1].split('>')
    return pieces[1]

def getPlayerSeasons(playerPage):
    '''Returns a list of the urls for season in which the player played.
    Args: the URL of a player's career page
    Returns: list of URLS for each season he played'''
    playerSeasons = []
    parser = getUrls(playerPage)
 
    for url in parser.urls:
        if "/players/player_byseason.htm?yr=" in url:
            playerSeasons.append('http://www.databasegolf.com'+ url)
    return playerSeasons


def ExtractDataFromHyperlink(LineOfHTML):
    '''Some table entries contain hyperlinks. This function parses & 
    returns the text of a hyperlink'''
    partial = LineOfHTML.split("<")
    complete = partial[1].split(">")
    return complete[1]

def ExtractRoundScores(scores):
    '''Scores are written as 'r1, r2, r3, r4 = total'. This function
    parses that into a tuple of 4 integers, one score for each round, 
    discarding the total score'''
    partial = scores.split(',')
    last = (partial[3].split('='))[0].split()
    scores = (int(partial[0]), int(partial[1]), int(partial[2]), int(last[0]))
    return scores
    
    
def BuildTableRow(player, row, t):
    date = row[0]
    tourn = ExtractDataFromHyperlink(row[1])
    scoreToPar = ExtractDataFromHyperlink(row[2])
    roundScores = ExtractRoundScores(row[3])
    finish = row[4]
    earnings = ExtractDataFromHyperlink(row[5])
    
    new = [player, date, tourn, scoreToPar,roundScores, finish, earnings, t]

    return new
		
def makeTournLevelPlayerTable_ByPlayer():
    playerPages = getPlayerCareerURLS()
    summary = []
    for page in playerPages:
        table = getMainTable(page)
        
        #gets player info off career summary page
        player = getPlayerName(page)
        seasons = getPlayerSeasons(page)
        filename = player +'.csv'
        writer = csv.writer(open(filename,"wb")) 
        y = 1
        t = 1
        for s in seasons:
            tournTable = getMainTable(s)
            for row in tournTable:
                newRow = BuildTableRow(player, row, t)
                writer.writerow(newRow)
                t += 1
            y += 1
        print 'Done with ', player
        summary.append([player, y, t])
    sum_writer = csv.writer(open("summary.csv", "wb"))
    for row in summary:
        sum_writer.writerow(row)
        
        
def makeYearLevelPlayerTable():
    #Get a list of the career pages for every player
    playerPages = getPlayerCareerURLS()

    masterTable = []
    writer = csv.writer(open("overview.csv", "wb"))
    for page in playerPages:
        '''Looks at each player's career page, gets each player/year page'''
        table = getMainTable(page)
        player = getPlayerName(page)
        print 'Writing rows for ', player
        i = 1
        for row in table:
             newRow = []
             newRow.append(player)
             newRow.append(getYear(row[0]))
             newRow.extend(row[1:])
             newRow.append(i)
             i += 1
             writer.writerow(newRow)
    print 'Done making general table'
    return 0

def makeSummaryTable():
    
    ## THIS IS FUBAR################
    playerPages = getPlayerCareerURLS()
    
    writer = csv.writer(open("years.csv","wb"))
    totalSeasons = {}
    totalTourneys = {}
    for page in playerPages:
        table = getMainTable(page)
        player = getPlayerName(page)
        seasons = getPlayerSeasons(page)
        totalSeasons[player] = 0
        totalTourneys[player] = 0        
        for s in seasons:
            table = getMainTable(s)
            totalSeasons[player] = totalSeasons[player] + 1
            for row in table:
				totalTourneys[player] += 1

    return totalSeasons, totalTourneys


def ParseCareerYears(ahref):
    pieceA = ahref.split('(')[1]
    startYear = pieceA.split('-')[0]
    startYear.strip()
    print startYear
    
    endYear = pieceA.split('-')[1]
    
    endYear = endYear.split(')')[0]
    endYear.strip()
    print endYear
    years = float(endYear) - float(startYear)
    return years

def ParsePlayerName(ahref):
    pieceA = ahref.split('<')[1]
    pieceB = pieceA.split('>')[1]
    last = pieceB.split(',')[0]
    first = pieceB.split(';')[1]
    name = first + last
    return name    
def CorrectlyMakeSummaryTable():
    lastInitialPages = getLastInitialUrls()
    writer = csv.writer(open("summary.csv", "wb"))
    for url in lastInitialPages:
        table = getMainTable(url)
        for row in table:
            name = ParsePlayerName(row[0])
            years = ParseCareerYears(row[0])
            tournaments = row[1]
            cutsMade = row[2]
            wins = row[3]
            newRow = [name, years, tournaments, cutsMade, wins]
            print newRow
            writer.writerow(newRow)
            
            


def getCollegeName(page):
    """Takes a player's career page & returns college name. Returns 0 if none
    is listed"""
    html = getHTMLSource(page)
    partial = html.split('College:')
    if len(partial) == 1: return 'NA'
    else:
        partial2 = partial[1].split('>')[1]
        complete = partial2.split('<')[0]
    return complete.strip()
    
 

def makeCollegeList():
    playerPages = getPlayerCareerURLS()
    writer = csv.writer(open("colleges.csv", "wb"))
    for page in playerPages:
        player = getPlayerName(page)
        college = getCollegeName(page)
        row = [player, college]
        writer.writerow(row)
        print row
        

#makeCollegeList()
#------------ Analysis 1:--------------------#
#makeYearLevelPlayerTable()   
makeTournLevelPlayerTable_ByPlayer()












#--------------Potential TrashCan-------------#


def makeTournLevelPlayerTable_Complete():
    '''Returns a master csv file containing every tournament for every
    player. Disused in favor of one csv file per player, because trying
    to open the master csv file would crash the computer
    Args: none
    Returns: years.csv'''
    playerPages = getPlayerCareerURLS()
    writer = csv.writer(open("years.csv","wb"))
    for page in playerPages:
        table = getMainTable(page)
        player = getPlayerName(page)
        seasons = getPlayerSeasons(page)
        print 'Got a list of seasons for ', player
        i = 1
        for s in seasons:
            print 'working on ', player, ' for his ', i, 'th year'
            #html = getHTMLSource(s)
            table = getMainTable(s)

            for row in table:
                newRow = []
                newRow.append(player)
                newRow.extend(row)
                writer.writerow(newRow)
            i += 1
        print 'Done with ', player    

def parsePlayer():
    players = getPlayerPage()
    return getUrls(players[0]).urls

class Player:
    def __init__(self,blah):
        pass
    '''will need a list of year summarys, a list of tournaments'''
class YearSummary:
    def __init__(self,data):
        self.season = self.getYear(data[0])
        self.age = data[1]
        self.totalTourns = data[2]
        self.cutsMade = data[3]
        self.topTens = data[4]
        self.majorsWon = data[5]
        self.highestFinish = data[6]
        self.driving = data[7]
        self.fairways = data[8]
        self.greens = data[9]
        self.putts = data[10]
        self.avgScore = data[11]
        self.earnings = data[12]
        self.earningsRank = data[13]

        
class Tourney:
    def __init__(self, row, player):
        self.date = row[0]
        self.tournname = row[1]
        self.toPar = row[2]
        self.score = Score(row[3])
        self.finish = row[4]
        self.earnings = row[5]
        self.player = player
 
class Score:
    def __init__(self, entry):
        self.cumulative = self.processScore(entry)
        self.round1 = self.cumulative[0]
        self.round2 = self.cumulative[1]
        self.round3 = self.cumulative[2]
        self.round4 = self.cumulative[3]
        self.total = self.cumulative[4]

    def processScore(self, entry):
        return entry.split(', =')

