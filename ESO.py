import matplotlib.pyplot as plt

# Definizione delle linee
linea1 = [(450.0, 562.5), (476.4371, 568.21932), (451.83944, 564.05655), (424.94795, 558.63273), (420.6674, 556.5881), (418.86824, 556.44092), (418.55057, 556.09838), (441.10038, 573.09484), (470.78525, 583.07818), (551.76318, 600.26085), (552.01926, 597.64664), (612.31179, 605.29408), (652.57463, 605.42611), (745.09429, 618.32118), (775.65692, 621.0074), (775.15111, 619.9835), (828.42712, 621.5356), (873.08274, 613.88216), (900.13301, 617.36901), (947.88868, 609.00082), (942.61525, 608.18309), (985.7363, 604.3752), (998.40196, 602.93688), (1041.88871, 598.68116), (1040.9532, 599.05929), (1081.6913, 594.30246), (1126.64997, 593.1784), (1147.32426, 590.94087), (1195.59189, 587.24538), (1196.02909, 587.41894), (1235.57797, 582.71872), (1250.21616, 580.68667), (1277.34243, 576.25903), (1276.72679, 576.20085), (1305.04928, 573.36894), (1329.9553, 570.6041), (1348.93746, 567.74641), (1346.76752, 568.42707), (1372.45548, 563.66633), (1391.46579, 563.08381), (1395.1187, 562.5), (1400.59967, 561.62404), (1426.0858, 561.27406), (1423.4907, 561.00286), (1445.22227, 557.00588), (1470.0, 562.5)]
linea2 = [(450.0, 562.5), (482.35985, 562.5), (1395.1187, 562.5), (1470.0, 562.5)]
#linea2 = [(0.0, 0.0), (0.0, 1.0), (1.0, -1.0), (2.0, 1.0), (3.0, -1.0), (4.0, 1.0), (5.0, -1.0), (6.0, 1.0), (7.0, -1.0), (8.0, 1.0), (9.0, -1.0), (10.0, 1.0)]
#linea3 = [(0.0, 0.0), (0.0, 1.0), (1.0, -1.0), (2.0, 1.0), (3.0, -1.0), (4.0, 1.0), (5.0, -1.0), (6.0, 1.0), (7.0, -1.0), (8.0, 1.0), (9.0, -1.0), (10.0, 1.0)]


#inea4 = [(450.0, 562.5), (426.67860965535624, 548.3109492509031), (444.28717073209486, 564.1772477245606), (467.7852640367217, 567.0195777896043), (471.3510768753168, 566.4366175466423), (502.9059969201479, 569.2223023707949), (538.2922942747434, 571.3998836721721), (552.0521223428001, 567.748707556697), (593.1186743237965, 572.7305927155553), (634.1274025848388, 566.3455602715366), (673.1574744801765, 569.097830274301), (682.049760279719, 569.0460473502047), (737.5010104776334, 574.1637151764936), (796.4203185042946, 586.1285185952619), (809.296084205624, 585.4935385856752), (859.0773561129595, 585.6184822363947), (907.360396489104, 581.2574656981435), (921.2699502058565, 580.9360162867633), (973.2729962282341, 573.5935720048649), (1020.9968724353041, 572.6538148122278), (1033.1677305331477, 572.786952233338), (1086.8187072603707, 563.4309320208441), (1134.8935600065552, 564.8240744209277), (1176.452245744781, 563.9797881010595), (1191.8924360016404, 569.7040931280512), (1240.6687543747796, 567.7664956729453), (1294.5123090475904, 564.1042438317951), (1302.686162259053, 562.5), (1307.524001331477, 561.5505000162873), (1331.4028809130912, 551.9042904290429), (1343.8609030401813, 549.4061947844599), (1348.3606652024253, 546.5492605331661), (1374.052274015213, 548.4807576062866), (1403.5576312972582, 549.4844675230026), (1410.6191615246476, 549.3583506754086), (1434.3016015604564, 562.5), (1438.2828396033, 564.7092332613389), (1470.0, 562.5)]

#linea5 = [(450.0, 562.5)]
#curve_points = [ (0.0, 0.0), (1.0, 0.5), (2.0, 1.0), (1.5, 1.5), (2.5, 0.8), (3.0, -0.5), (4.0, 0.2), (3.2, 1.0), (5.0, 0.5), (6.0, 1.2), (5.5, 0.0),  (7.0, 1.0), (8.0, 0.3), (9.0, 1.5), (10.0, 1.0) ]


def insert_intersections_corrected(line1, line2):
    """
    Trova le intersezioni tra i segmenti di due linee e aggiorna la seconda linea
    inserendo le intersezioni nel punto corretto, gestendo anche intersezioni esatte sugli endpoint.
    """
    def is_intersecting(p1, p2, q1, q2):
        """Calcola se due segmenti si intersecano e il punto di intersezione."""
        det = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
        if det == 0:
            return False, None  # Segmenti paralleli o coincidenti

        t = ((q1[0] - p1[0]) * (q2[1] - q1[1]) - (q1[1] - p1[1]) * (q2[0] - q1[0])) / det
        u = ((q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])) / det

        if 0 <= t <= 1 and 0 <= u <= 1:
            # Calcolo punto di intersezione
            intersection = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
            return True, intersection

        return False, None

    updated_line2 = line2.copy()
    insert_positions = []  # Traccia le posizioni dove inserire gli aggiornamenti

    for i in range(len(line1) - 1):
        p1, p2 = line1[i], line1[i + 1]
        for j in range(len(updated_line2) - 1):
            q1, q2 = updated_line2[j], updated_line2[j + 1]
            intersect, point = is_intersecting(p1, p2, q1, q2)
            if intersect and point not in updated_line2:
                insert_positions.append((j + 1, point))  # Traccia posizione e punto

    # Inserire i punti nella posizione corretta senza interferire con l'iterazione
    for pos, point in sorted(insert_positions, reverse=True):
        updated_line2.insert(pos, point)

    return updated_line2


# Calcola la nuova linea aggiornata con il fix
linea3 = insert_intersections_corrected(linea2, linea1)

# Separazione delle coordinate per il plotting
def extract_coords(line):
    x, y = zip(*line)
    return x, y

x1, y1 = extract_coords(linea1)
x2, y2 = extract_coords(linea2)
x3, y3 = extract_coords(linea3)
# x4, y4 = extract_coords(linea4)
# x5, y5 = extract_coords(linea5)

# Separazione delle coordinate per il plotting
#x2_updated_corrected, y2_updated_corrected = zip(*updated_line2_corrected)

# Plot delle linee con correzione
plt.figure(figsize=(12, 6))
plt.plot(x1, y1, label='Linea 1 (Checkpoint)', marker='o', linestyle='-', color='blue')
#plt.plot(x2, y2, label='Linea 2 (percorso utente)', marker='o', linestyle='--', color='green')
#plt.plot(x3, y3, label='Linea 3 (intersezione utente e linea ideale', marker='o', linestyle=':', color='red')
#plt.plot(x4, y4, label='Linea 4 (Aggiornata)', marker='o', linestyle=':', color='yellow')
#plt.plot(x5, y5, label='Linea 5 (Box)', marker='o', linestyle=':', color='purple')
plt.plot(482.35985, 562.5, label='Punto critico', marker='o', linestyle=':', color='black')


# Personalizzazione del grafico
plt.title('Aggiornamento della Linea con Intersezioni (Corretto)')
plt.xlabel('X')
plt.ylabel('Y')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Linea dello zero
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()

#print(linea3)