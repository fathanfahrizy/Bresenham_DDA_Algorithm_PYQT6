# algoritma_garis.py

class AlgoritmaGaris:
    """
    Kelas statis untuk menampung algoritma perhitungan garis.
    Mengembalikan list berisi tuple koordinat (x, y) per piksel.
    """

    @staticmethod
    def dda(x1, y1, x2, y2):
        koordinat_piksel = []
        dx = x2 - x1
        dy = y2 - y1
        
        # Tentukan steps (langkah) dari selisih terbesar
        steps = max(abs(dx), abs(dy))
        
        # Jika titik awal dan akhir sama
        if steps == 0:
            return [(x1, y1)]
            
        x_inc = dx / steps
        y_inc = dy / steps
        
        x = x1
        y = y1
        
        # Hitung titik per step
        for _ in range(int(steps) + 1):
            koordinat_piksel.append((round(x), round(y)))
            x += x_inc
            y += y_inc
            
        return koordinat_piksel

    @staticmethod
    def bresenham(x1, y1, x2, y2):
        koordinat_piksel = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        # Tentukan arah maju/mundur
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        err = dx - dy
        
        while True:
            koordinat_piksel.append((x1, y1))
            
            # Berhenti jika titik saat ini sama dengan titik akhir
            if x1 == x2 and y1 == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
        return koordinat_piksel