class Histo:
    def __init__(self,XMLHisto):
        self.Title,self.nbins,self.xmin,self.xmax= self.parse_description(XMLHisto.find("Description").text)
        self.NEvents,self.TotalWeight,self.NEventsInHisto,self.TotalWeightInHisto=self.parse_statistics(XMLHisto.find("Statistics").text)
        self.Underflow,self.Data,self.Overflow,self.DataNorm=self.parse_data(XMLHisto.find("Data").text)
    def parse_description(self,DescriptionText):
        title,blah,struct=DescriptionText.strip("\n").split("\n")
        struct=[int((struct.split())[0]),float((struct.split())[1]),float((struct.split())[2])]
        struct.insert(0,title.strip("\""))
        return struct
    def parse_statistics(self,StatisticsText):
        textlines=StatisticsText.strip("\n").split('\n')
        return [ (x.split())[0] for x in textlines[0:4]]
    def parse_data(self,DataText):
        datatmp=[float((x.split())[0]) for x in DataText.strip("\n").split('\n')]
        return datatmp[0],\
        datatmp[1:self.nbins],\
        datatmp[self.nbins+1],\
        sum(datatmp[1:self.nbins])
