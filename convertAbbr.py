sourceFile = open('/Users/David/Desktop/UNT.xml','r',encoding='UTF-8').read()
sourceFile = sourceFile.replace("{ABB}PRX{/ABB}","prox")
sourceFile = sourceFile.replace("{ABB}1SG.SUB{/ABB}","1sg.sub")
sourceFile = sourceFile.replace("{ABB}AGT{/ABB}","agt")
sourceFile = sourceFile.replace("{ABB}AMB{/ABB}","amb")
sourceFile = sourceFile.replace("{ABB}INTR{/ABB}","intr")
sourceFile = sourceFile.replace("{ABB}INST{/ABB}","inst")
sourceFile = sourceFile.replace("{ABB}ADD{/ABB}","add")
sourceFile = sourceFile.replace("{ABB}ADV{/ABB}","adv")
sourceFile = sourceFile.replace("{ABB}ADJ{/ABB}","adj")
sourceFile = sourceFile.replace("{ABB}ALN{/ABB}","aln")
sourceFile = sourceFile.replace("{ABB}ALTV{/ABB}","altv")
sourceFile = sourceFile.replace("{ABB}APL{/ABB}","apl")
sourceFile = sourceFile.replace("{ABB}AUG{/ABB}","aug")
sourceFile = sourceFile.replace("{ABB}BEN{/ABB}","ben")
sourceFile = sourceFile.replace("{ABB}BYPD{/ABB}","bypd")
sourceFile = sourceFile.replace("{ABB}CBEN{/ABB}","cben")
sourceFile = sourceFile.replace("{ABB}CLF{/ABB}","clf")
sourceFile = sourceFile.replace("{ABB}CMT{/ABB}","cmt")
sourceFile = sourceFile.replace("{ABB}CNN{/ABB}","cnn")
sourceFile = sourceFile.replace("{ABB}CS{/ABB}","cs")
sourceFile = sourceFile.replace("{ABB}DEB{/ABB}","deb")
sourceFile = sourceFile.replace("{ABB}DCS{/ABB}","dcs")
sourceFile = sourceFile.replace("{ABB}DTRN{/ABB}","dtrn")
sourceFile = sourceFile.replace("{ABB}DEM{/ABB}","dem")
sourceFile = sourceFile.replace("{ABB}DIM{/ABB}","dim")
sourceFile = sourceFile.replace("{ABB}DSD{/ABB}","dsd")
sourceFile = sourceFile.replace("{ABB}DST{/ABB}","dst")
sourceFile = sourceFile.replace("{ABB}DTV{/ABB}","dtv")
sourceFile = sourceFile.replace("{ABB}3PO{/ABB}","3po")
sourceFile = sourceFile.replace("{ABB}DYN{/ABB}","dyn")
sourceFile = sourceFile.replace("{ABB}GNC{/ABB}","gnc")
sourceFile = sourceFile.replace("{ABB}IDF{/ABB}","idf")
sourceFile = sourceFile.replace("{ABB}IHB{/ABB}","ihb")
sourceFile = sourceFile.replace("{ABB}IMPF{/ABB}","impf")
sourceFile = sourceFile.replace("{ABB}INTNS{/ABB}","intns")
sourceFile = sourceFile.replace("{ABB}LOC{/ABB}","loc")
sourceFile = sourceFile.replace("{ABB}LOCDST{/ABB}","locdst")
sourceFile = sourceFile.replace("{ABB}NEG{/ABB}","neg")
sourceFile = sourceFile.replace("{ABB}NM{/ABB}","nm")
sourceFile = sourceFile.replace("{ABB}DEB{/ABB}","deb")
sourceFile = sourceFile.replace("{ABB}OPT{/ABB}","optv")
sourceFile = sourceFile.replace("{ABB}PFV{/ABB}","pfv")
sourceFile = sourceFile.replace("{ABB}PL{/ABB}","pl")
sourceFile = sourceFile.replace("{ABB}PLACE{/ABB}","plc")
sourceFile = sourceFile.replace("{ABB}PL.PO{/ABB}","pl.po")
sourceFile = sourceFile.replace("{ABB}PROX{/ABB}","prox")
sourceFile = sourceFile.replace("{ABB}PXM{/ABB}","pxm")
sourceFile = sourceFile.replace("{ABB}RCP{/ABB}","rcp")
sourceFile = sourceFile.replace("{ABB}REL{/ABB}","rel")
sourceFile = sourceFile.replace("{ABB}RT{/ABB}","rt")
sourceFile = sourceFile.replace("{ABB}SEM{/ABB}","sem")
sourceFile = sourceFile.replace("{ABB}STM{/ABB}","stm")
sourceFile = sourceFile.replace("{ABB}SUBST{/ABB}","subst")
sourceFile = sourceFile.replace("{ABB}TRNS{/ABB}","trns")
sourceFile = sourceFile.replace("{ABB}VBL{/ABB}","vbl")
sourceFile = sourceFile.replace("{ABB}CTNR{/ABB}","ctnr")
sourceFile = sourceFile.replace("{ABB}2SG.SUB{/ABB}","2sg.sub")
sourceFile = sourceFile.replace("{ABB}2SUB{/ABB}","2sub")
sourceFile = sourceFile.replace("{ABB}:NM{/ABB}",":nm")
sourceFile = sourceFile.replace("{ABB}:PFV{/ABB}",":pfv")
sourceFile = sourceFile.replace("{ABB}–PFV{/ABB}","–pfv")
sourceFile = sourceFile.replace("{ABB}PL.OBJ–/ABB}","pl.obj–")
sourceFile = sourceFile.replace("{ABB}–PL.PO{/ABB}","–pl.po")
sourceFile = sourceFile.replace("{ABB}IDF:PFV{/ABB}","idf:pfv")
newFile = open('/Users/David/Desktop/NewUNT.xml',"w",encoding="UTF-8")
newFile.write(sourceFile)
newFile.close()
