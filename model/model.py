from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._clientiMaxBest = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()

    def worstCase(self, nerc, maxY, maxH):
        # questo è quello che succede quando viene schiacciato il bottone

        self.loadEvents(nerc) #carico eventi von il nerc selezionato
        parziale = [] #inizializzo l'array parziale
        self.ricorsione(parziale, maxY, maxH, 0)

        print(self._solBest)

    def ricorsione(self, parziale, maxY, maxH, pos):
        #pos sarebbe la posizione dell'evento da considerare dalla lista degli eventi

        # terminazione: se la somma della durata degli eventi supera le y ore esce dalla ricorsione
        if self.sumDurata(parziale)/60/60 > maxH:
            return

        # verifica se best: verifica se la soluzione attuale è meglio di quella migliore
        if self.countCustomers(parziale) > self._clientiMaxBest:
            self._solBest = parziale[:] #come copy
            self._clientiMaxBest = self.countCustomers(parziale)

        # ricorsione
        i = pos
        for e in self._listEvents[pos:]: #i, e in enumerate(self._listEvents[pos:]):
            parziale.append(e)
            #vincoli
            if self.getRangeAnni(parziale) > maxY:
                parziale.remove(e) #lo rimuovo subito se non supera i vincoli
                return
            i+=1 #passo all'evento successivo, e rifaccio le stesse cose
            self.ricorsione(parziale, maxY, maxH, i)
            parziale.remove(e)#backtracking


    def getRangeAnni(self, listOutages):
        if len(listOutages) < 2:
            return 0

        first = listOutages[0].date_event_began
        last = listOutages[-1].date_event_finished
        return int(last.year - first.year)

    def countCustomers(self, listOutages):
        if len(listOutages) == 0:
            return 0

        numCustomers = 0
        for event in listOutages:
            numCustomers += event.customers_affected
        return numCustomers

    def sumDurata(self, listOutages):
        if len(listOutages)==0:
            return 0

        sum = 0
        for event in listOutages:
            sum += self.durata(event)
        return sum
    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    def durata(self, event):
        return (event.date_event_finished - event.date_event_began).total_seconds()

    @property
    def listNerc(self):
        return self._listNerc