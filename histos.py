import copy

class Histo:
######## INIT Stuff
    def __init__(self,XMLHisto):
        self.Title,self.nbins,self.xmin,self.xmax= self.parse_description(XMLHisto.find("Description").text)
        self.NEvents,self.TotalWeight,self.NEventsInHisto,self.TotalWeightInHisto=self.parse_statistics(XMLHisto.find("Statistics").text)
        self.Underflow,self.Data,self.Overflow,self.DataNorm=self.parse_data(XMLHisto.find("Data").text)
        self.binning()

    def parse_description(self,DescriptionText):
        title,blah,struct=DescriptionText.strip("\n").split("\n")
        struct=[int((struct.split())[0]),float((struct.split())[1]),float((struct.split())[2])]
        struct.insert(0,title.strip("\""))
        return struct

    def parse_statistics(self,StatisticsText):
        textlines=StatisticsText.strip("\n").split('\n')
        return [ float((x.split())[0]) for x in textlines[0:4]]

    def parse_data(self,DataText):
        datatmp=[float((x.split())[0]) for x in DataText.strip("\n").split('\n')]
        return datatmp[0],\
        datatmp[1:self.nbins+1],\
        datatmp[self.nbins+1],\
        sum(datatmp) #Need to consider over and underflow for proper normalization

    def binning(self):#Determine the left hand limit of the bins
        self.binsize=(self.xmax-self.xmin)/self.nbins
        self.lbins=[self.xmin+self.binsize*i for i in range(self.nbins)]#range(self.xmin,self.xmax,self.binsize)#left limit of the bins

######## Printing

    def __repr__(self):
        return """Histogram: {}, {} bins in [{},{}]""".format(self.Title,self.nbins,self.xmin,self.xmax)

    def __str__(self):
        out=""
        for l in self.Data:
            out+="{}\n".format(l)
        return out

    def Mathematica(self):#provide an output that can make a Mathematica histogram
        points=zip(self.lbins,self.Data)
        spoints=["{{{},{}}}".format(str(x),str(y)) for (x,y) in points]
        spoints=",".join(spoints)
        mathematica_output="ListStepPlot[{{{}}}, PlotRange -> Full, PlotRangePadding -> {{None, {{1, 1}}}}, Frame -> True]".format(spoints)
        print mathematica_output


######## Histogram manipulation

    def __add__(self,H2):
        if self.nbins==H2.nbins and self.xmin==H2.xmin and self.xmax==H2.xmax:
            H3=copy.copy(self)
            H3.Title+="+"+H2.Title
            H3.Underflow+=H2.Underflow
            H3.Overflow+=H2.Overflow
            H3.DataNorm+=H2.DataNorm
            H3.NEvents+=H2.NEvents
            H3.TotalWeight+=H2.TotalWeight
            H3.NEventsInHisto+=H2.NEventsInHisto
            H3.TotalWeightInHisto+=H2.TotalWeightInHisto
            H3.Data = [sum(x) for x in zip(H3.Data,H2.Data)]
            return H3

    def __sub__(self,H2):
        if self.nbins==H2.nbins and self.xmin==H2.xmin and self.xmax==H2.xmax:
            H3=copy.copy(self)
            H3.Title+="-"+H2.Title
            H3.Underflow-=H2.Underflow
            H3.Overflow-=H2.Overflow
            H3.DataNorm-=H2.DataNorm
            H3.NEvents-=H2.NEvents
            H3.TotalWeight-=H2.TotalWeight
            H3.NEventsInHisto-=H2.NEventsInHisto
            H3.TotalWeightInHisto-=H2.TotalWeightInHisto
            H3.Data = [x-y for (x,y) in zip(H3.Data,H2.Data)]
            return H3

    def __mul__(self,H2):
        if self.nbins==H2.nbins and self.xmin==H2.xmin and self.xmax==H2.xmax:
            H3=copy.copy(self)
            H3.Title+="*"+H2.Title
            H3.Underflow=-1 #This is not really useful information anymore
            H3.Overflow=-1 #This is not really useful information anymore
            H3.DataNorm*=H2.DataNorm
            H3.NEvents*=H2.NEvents
            H3.TotalWeight*=H2.TotalWeight
            H3.NEventsInHisto*=H2.NEventsInHisto
            H3.TotalWeightInHisto*=H2.TotalWeightInHisto
            H3.Data = [x*y for (x,y) in zip(H3.Data,H2.Data)]
            return H3

    def __div__(self,H2):
        def divmax(x,y):
            z=max(x,y)
            if z==x:
                print "Warning: Replaced a zero value in the division"
            return z
        if self.nbins==H2.nbins and self.xmin==H2.xmin and self.xmax==H2.xmax:
            H3=copy.copy(self)
            H3.Title+="+"+H2.Title
            H3.Underflow=-1 #This is not really useful information anymore
            H3.Overflow=-1 #This is not really useful information anymore
            H3.DataNorm/=H2.DataNorm
            H3.NEvents/=H2.NEvents
            H3.TotalWeight/=H2.TotalWeight
            H3.NEventsInHisto/=H2.NEventsInHisto
            H3.TotalWeightInHisto/=H2.TotalWeightInHisto
            y0=min([y for y in H2.Data if y!=0])/10.
            H3.Data = [x/divmax(y0,y) for (x,y) in zip(H3.Data,H2.Data)]
            return H3

    def Normalize(self):
        H3=copy.copy(self)
        H3.Data=[d/H3.DataNorm for d in H3.Data]
        H3.Underflow/=H3.DataNorm
        H3.Overflow/=H3.DataNorm
        H3.DataNorm=1
        return H3
