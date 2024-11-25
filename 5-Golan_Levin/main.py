import tkinter as tk
from tkinter import Canvas
import time
import threading
from PIL import Image, ImageTk, ImagePalette
import numpy as np
import pygame
from pygame.locals import *

class CountryHighlighterApp:
    
    countryNames = [
        "United States of America","Canada","Mexico","Guatemala","Cuba","Haiti","Dominican Republic","Belize",
        "Honduras","Nicaragua","Costa Rica","Panama","Colombia","Venezuela","Guyana","Suriname",
        "French Guyana","Ecuador","Peru","Bolivia","Chile","Argentina","Uruguay","Andorra",
        "Paraguay","Brazil","Morocco","Armenia","Mauritania","Senegal","Gambia","Guinea-Bissau",
        "Guinea","Sierra Leone","Liberia","Cote d'Ivoire","Ghana","Togo","Benin","Nigeria",
        "Cameroon","Equatorial Guinea","Gabon","Republic of the Congo",
        "Democratic Republic of Congo","Angola","Namibia","South Africa",
        "Mozambique","Tanzania","Kenya","Somalia","Ethiopia","Sudan","Egypt","Libya",
        "Tunisia","Algeria","Mali","Burkina Faso","Niger","Chad","Central African Republic","Uganda",
        "Rwanda","Burundi","Zambia","Malawi","Zimbabwe","Botswana","Swaziland","Lesotho",
        "Madagascar","Greece","Albania","Yugoslavia","Italy","Spain","Portugal","France",
        "United Kingdom","Ireland","Azerbaijan","Belgium","Netherlands","Denmark","Germany","Switzerland",
        "Austria","Hungary","Czech Republic","Poland","Sweden","Norway","Finland","Romania",
        "Bulgaria","Turkey","Syria","Israel","Jordan","Iraq","Bahrain","Kuwait",
        "Saudi Arabia","Belarus","Yemen","Oman","United Arab Emirates","Iran","Afghanistan","Pakistan",
        "India","Sri Lanka","Nepal","Bosnia and Herzegovina","Bhutan","Bangladesh","Croatia","Cyprus",
        "Burma","Thailand","Laos","Cambodia","Vietnam","Off-One Error","Malaysia","Singapore",
        "Indonesia","Djibouti","Brunei","El Salvador","Hong Kong","Eritrea","Estonia","Philippines",
        "Georgia","Papua New Guinea","Australia","Gibraltar","New Zealand","China","North Korea","South Korea",
        "Mongolia","Japan","Russia","Greenland","Iceland","Kazakhstan","Kyrgyzstan","Latvia",
        "Lebanon","Liechtenstein","Lithuania","Luxembourg","Macedonia","Moldova",
        "Monaco","Qatar","Slovak Republic","Slovenia","Taiwan","Tajikistan","Turkmenistan",
        "Ukraine","Uzbekistan","Antigua and Barbuda","Bahamas","Barbados","Bermuda","Cape Verde",
        "Dominica","Grenada","Guadeloupe","Guam","Jamaica","Malta","Mauritius","New Caledonia","Palau",
        "Puerto Rico","Reunion","Seychelles","Trinidad and Tobago"]
    letStr = " whose names start with the letter "
    # The set of properties a country can have.
    propNames = [
        "itsy-bitsy","small","huge","densely-populated",
        "sparsely-populated","long and skinny","peninsular","island-dwell",
        "landlocked","rainy","arid","cloudy",
        "earthquake-prone","officially polylingual","officially Anglophone","Portuguese-speak",
        "politically or territorially dependent","largely illiterate","heavily-indebted and poor","monarchic",
        "dictatorially autocratic","communist","Slavic","predominantly Muslim",
        "predominantly Catholic","predominantly Orthodox","predominantly Buddhist","Scandinavian",
        "Baltic","Mediterranean","South Asian","Southeast Asian",
        "Sub-Saharan African","Southern African","South American","Central American",
        "South Pacific","East Asian","Middle Eastern","Central European",
        "North African","Balkan","former Soviet","China-neighboring",
        "camel-driv","tiger-roamed","pachyderm-keep","Olympic badminton medal winn",
        "oil-produc","vodka-export","nuclear-powered","juvenile-offender execut",
        "tourism-dependent","Olympic judo Silver medal winn","violence-ravaged","pepper-produc",
        "cricket-play","oil-guzzl","cannabis-cultivat","bug-eat",
        "least corrupt","insufficiently-reproducing","fermented mare's milk drink","orange-white-and-green flag-wav",
        "US visa-waiver pilot-program participat","US bullet-buy","ancient pyramid-maintain","hydroelectric",
        "border-disput","AIDS crisis-stricken","perceived as egregiously corrupt","undersexed",
        "heavily landmined","person-traffick","shark-infested","Simpsons' travel destination",
        "former French colony","comparatively depressed","comparatively happy","former Ottoman",
        "former Sassanid","former Habsburg","former Roman","frequently lightning-struck",
        "Australopithecus fossil-hous","population-skyrocket","EU","UN Security Council Permanent Member",
        "G7","Fishery Committee for the Eastern Central Atlantic member"]
    nSelectedCountries = 0
    nCountries = countryNames.length
    nProperties = propNames.length
    nProperties2 = nProperties-63
    # Codes for the syntactic combination of properties:
    # which properties are verbs, adjectives, etc. 
    propVerbs = [
        0,0,0,0, 0,0,0,1, 0,0,0,0, 0,0,0,1,
        0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 
        0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,1,1,
        1,1,0,1, 0,1,0,1, 1,1,1,1, 0,0,1,1,
        1,1,1,0, 1,0,0,0, 0,1,0,0, 0,0,0,0, 
        0,0,0,0, 1,1,0,0, 0,0,0,0, 0,1]
    propAdjs = [
        1,1,1,1, 1,1,0,0, 1,1,1,1, 1,1,1,0,
        1,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 
        0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0,
        0,0,0,0, 0,0,0,0, 0,0,0,0, 1,1,0,0, 
        0,0,0,0, 0,0,0,1, 1,0,1,0, 0,1,1,0, 
        0,0,0,1, 0,0,0,0, 0,0,0,0, 0,0]
    # Binary property subscriptions, per country, 
    # represented compactly as decimal Longs.
    # We have more property descriptors than bits in a Long,
    # so we split the property annotations across two arrays.
    
    countryProp1 = [
        481603685151961092L, 1668302186964082692L, 907193884314963968L, 869476237435731968L,
        9288674250326176L, 4503599644160128L, 4785074620858496L, 293296960109035522L,
        864691162831917056L, 576460786680205568L, 292734010155602432L, 4785108980597248L,
        883549969091400192L, 576742244476780544L, 864691145635282944L, 576742244460003344L,
        288230393348424192L, 576742244476787200L, 576742244476792832L, 576742244477042944L,
        576742244476784672L, 74027936071553024L, 17196646400L, 148618787720012033L,
        882705544161263872L, 875668669743530500L, 329062940018218016L, 2613798624001265920L,
        18691706455056L, 288318341385691648L, 4521191822213666L, 18084767254086144L,
        18084767262318592L, 18084771557294592L, 18084767253938688L, 288582219872862208L,
        288582224167845888L, 70373039415328L, 281479272071200L, 110690038886457344L,
        576812600320614912L, 351848033681410L, 576812600319279104L, 576812600319549440L,
        883057374981791744L, 594827003124023296L, 648606315861525520L, 938789424664174592L,
        882775904299024384L, 648588719380758528L, 941604170136576000L, 18102359448380416L,
        18103458951753984L, 18384933937742848L, 49840037998629888L, 300167220691984L,
        40832563865977856L, 54343362748093440L, 89060450510080L, 70373039546624L,
        89060450641152L, 18103458951603456L, 576531125342839040L, 666603117890257152L,
        18084771566215426L, 18014402821497090L, 576531129637814528L, 576531129637822720L,
        666603122184962304L, 576531129637560592L, 70377334661378L, 4503608217854210L,
        869194736672710784L, 185492010222751808L, 283674008358912L, 2342718430223798272L,
        266556803498651712L, 195625109368086528L, 149463212650172416L, 231653906386518016L,
        1235956622737041536L, 217017207060719744L, 306548239878849536L, 155092712184883202L,
        1407093408577103872L, 1369938711785515008L, 227150855961313280L, 1307451266821005568L,
        5348574330093824L, 2352849880096964864L, 2307813883810676992L, 9852173961658368L,
        1299007017654421504L, 1297881117747587168L, 1298725542677194752L, 2343842131103191040L,
        2352851529385381888L, 36310272540938304L, 299342585922560L, 99660009356420098L,
        5084416653657088L, 299342050239488L, 4802666799039627L, 299067171667970L,
        146666329939117056L, 2594922208379797760L, 2551141862999040L, 299342049575936L,
        72356936087502848L, 2551141862740992L, 4917948385283028224L, 75743158097572864L,
        938850989799141376L, 94645960986067072L, 364905920100573472L, 18016597536944128L,
        114350350663938L, 72444623213166600L, 22801672157802496L, 22517998707290242L,
        18410225985131008L, 869581758390599680L, 292848327205323552L, 869300283413889024L,
        576856578706377248L, 0L, 649046114070692352L, 1225260575836102793L,
        905751292838679168L, 18691706065922L, 281477133131779L, 288793360481652738L,
        76569989758402561L, 18033090207170560L, 2306691832458772480L, 288511853292712064L,
        2599425808002985984L, 653303491812946560L, 1946417124859724948L, 76561193682157569L,
        1374442379997638784L, 614723894391083012L, 325592883920896L, 767160186463850560L,
        4621282555981725968L, 767582398996545664L, 2605099288006494212L, 75920L,
        1302103242397718672L, 4900774013648769280L, 4900211063703732480L, 2306410357482061824L,
        18032266118702082L, 4503599644672257L, 2307818282138206208L, 1153484454577578241L,
        36030996079972610L, 288797724185198848L, 4503600181542921L, 299342049576002L,
        1970874613760256L, 1128098951081984L, 145522700465475720L, 4918225462213214464L,
        4611989483645043712L, 2596048108286640128L, 4621559632854254848L, 4503599627911297L,
        4785074604097664L, 581245826907521161L, 76561193665380481L, 45185L,
        2594073385382199425L, 2598576985010094209L, 4503599644213377L, 4503599644237953L,
        869757678035943554L, 4503600181043337L, 869194736672456841L, 68736319616L,
        4503601774878849L, 4785074620948608L, 8606777473L, 4503599644172417L,
        3175882179406217345L]
    countryProp2 = [
        117479460L,33558580L,268437516L,60L,67108864L,8224L,4L,134217764L,
        4194364L,164L,4194356L,536870932L,1048628L,4227120L,36L,48L,
        4202528L,148L,536870932L,134217892L,36L,36L,22L,524294L,
        537919504L,134223892L,336077344L,82976L,335552512L,67117056L,67108864L,68157440L,
        68165680L,68157440L,67108864L,71311489L,68157456L,68165632L,201334800L,67109024L,
        67117296L,67108896L,67117104L,68165680L,68157488L,528L,84L,2099300L,
        268438096L,2103472L,6291696L,4196384L,2097712L,1115184L,590376L,4784160L,
        598016L,598048L,268443664L,134225920L,8225L,2105344L,8272L,1048752L,
        48L,134225936L,80L,268435552L,4194884L,134217792L,96L,64L,
        269492272L,76088356L,589840L,524320L,109576198L,76283942L,545783814L,126357542L,
        59248678L,8421415L,131232L,143130630L,76316678L,8421414L,41943046L,524310L,
        9175062L,852004L,262180L,603979780L,8421382L,67108918L,8388614L,67960832L,
        134758404L,590884L,4718624L,4784164L,4718596L,4390944L,134218752L,196612L,
        4262916L,134235136L,0L,4194304L,4195364L,4326432L,132624L,538050720L,
        289L,16L,16L,135071248L,134217744L,134217888L,786996L,589856L,
        134218784L,1049124L,8208L,1058336L,1057328L,0L,269484064L,1048614L,
        1049760L,10240L,134217762L,2060L,2304L,544L,0L,536870948L,
        606224L,536872960L,38918L,524288L,22L,16777512L,48L,67108896L,
        268435456L,100669734L,16794784L,16L,32822L,32L,1072L,16L,
        599044L,524322L,32L,8912914L,269025280L,268517408L,268959746L,4195328L,
        262144L,786470L,288L,1072L,131105L,82048L,0L,0L,
        134217732L,134217732L,134217728L,67108864L,8208L,0L,8192L,0L,
        4L,268959744L,268443680L,10244L,536870912L,32768L,8192L,8224L,4L]
     
    def __init__(self, root):
        self.root = root
        self.root.title("Country Highlighter")
        self.canvas = Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Dibujar un rectángulo como ejemplo
        self.canvas.create_rectangle(0, 0, 800, 50, fill="lightgray")

        # Mostrar texto en el lienzo
        self.canvas.create_text(100, 30, text="Nombre del país", fill="black", anchor="w")

class AxisApplet:
    def __init__(self, root):
        # Inicialización de variables
        self.APP_W = 919
        self.APP_H = 476 + 64
        self.display_area = None
        self.src_img = None
        self.dst_img = None
        self.src_array = None
        self.loaded_src = False
        self.filtered = False
        self.cur_ctry_id = 0
        self.which_sel = [-1, -1, -1]
        self.highlights = [0 for _ in range(256)]  # Se asume 256 países como placeholder
        self.bxf = self.APP_W / 2
        self.byf = self.APP_H / 2
        self.bxa = 0.36
        self.bxb = 1.0 - self.bxa
        self.bya = 0.29
        self.byb = 1.0 - self.bya
        self.bh = 20

        # Configuración del lienzo
        self.canvas = tk.Canvas(root, width=self.APP_W, height=self.APP_H, bg="white")
        self.canvas.pack()

        # Cargar imagen inicial
        self.prepare_imaging("world.gif")
        self.draw_initial_state()

    def prepare_imaging(self, image_path):
        """Carga una imagen y prepara la visualización."""
        try:
            # Cargar imagen usando Pillow
            image = Image.open(image_path).resize((self.APP_W, self.APP_H))
            self.src_img = ImageTk.PhotoImage(image)
            self.display_area = self.src_img
            self.loaded_src = True
        except FileNotFoundError:
            print(f"Error: No se encontró la imagen {image_path}.")
            self.loaded_src = False

    def draw_initial_state(self):
        """Dibuja el estado inicial en el lienzo."""
        if self.loaded_src:
            self.canvas.create_image(0, 0, image=self.src_img, anchor=tk.NW)

        # Ejemplo de dibujar un rectángulo y texto
        self.canvas.create_rectangle(self.bxf - 50, self.byf - 20, self.bxf + 50, self.byf + 20, fill="gray")
        self.canvas.create_text(self.bxf, self.byf, text="Ejemplo de texto", fill="black", font=("Arial", 12))
    
    def start(self):
        """Inicia el hilo del applet."""
        self.stop_thread = False
        if self.thread is None:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        """Detiene el hilo del applet."""
        self.stop_thread = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def destroy(self):
        """Destructor simulado (no hace nada explícito)."""
        pass

    def update(self):
        """Actualiza la pantalla o realiza una acción."""
        self.paint()

    def paint(self):
        """Simula la acción de pintar (debería ser sobrescrito)."""
        print("Pintando...")  # Placeholder

    def compute(self):
        """Simula cálculos realizados durante el bucle."""
        print("Computando...")  # Placeholder

    def run(self):
        """Método del hilo principal."""
        while not self.stop_thread:
            try:
                then = time.time()

                # Realizar operaciones
                self.compute()
                self.update()

                # Dormir durante el tiempo mínimo
                time.sleep(self.MIN_SLEEP)

                # Ajustar el tiempo de pausa restante
                now = time.time()
                nap_time = self.MAX_PLAY_TIME - (now - then)
                if nap_time > 0:
                    time.sleep(nap_time)
            except Exception as e:
                print(f"Excepción en el hilo: {e}")
                break
    
    def prepare_imaging(self, image_name):
        try:
            # Cargar la imagen de fondo
            src_img = Image.open(image_name).convert("RGB")
            if src_img.size != (self.APP_W, self.APP_H):
                src_img = src_img.resize((self.APP_W, self.APP_H))

            # Obtener los valores de los píxeles para pruebas futuras
            self.src_array = np.array(src_img)
            self.loaded_src = True

            # Construir una paleta de colores interpolada
            palr = []
            palg = []
            palb = []
            curr = []
            curg = []
            curb = []

            for i in range(self.NCOL):
                fi = i / (self.NCOL - 1)
                curr.append(0)
                curg.append(0)
                curb.append(0)
                palr.append(int(self.BASE + 40.0 * (fi**9.0)))
                palg.append(int(self.BASE + 80.0 * (fi**6.0)))
                palb.append(int(self.BASE + 120.0 * (fi**3.0)))

            # Crear una paleta para la nueva imagen
            palette = []
            for r, g, b in zip(palr, palg, palb):
                palette.extend([r, g, b])
            palette.extend([0] * (768 - len(palette)))  # Completar a 256 colores

            self.palette = palette
            colu = (palr[-1] & self.FF, palg[-1] & self.FF, palb[-1] & self.FF)

            # Crear la imagen con la paleta
            paletted_image = Image.fromarray(self.src_array, mode="P")
            paletted_image.putpalette(self.palette)
            self.dst_img = paletted_image

        except Exception as e:
            print(f"Error al preparar la imagen: {e}")
            
    def compute(self):
        if self.loaded_src:
            # Actualizar países resaltados
            self.highlight_country_at_cursor(self.csrX, self.csrY)
            for i in range(self.nCountries):
                vali = max(0, self.highlites[i] - self.PDEC)
                self.highlites[i] = vali
                self.curr[i] = self.palr[vali]
                self.curg[i] = self.palg[vali]
                self.curb[i] = self.palb[vali]

            # Resaltar los países seleccionados
            nSelected = 0
            for i in range(3):
                which = self.whichSel[i]
                if 0 <= which < self.nCountries:
                    self.curr[which] = self.FF
                    self.curg[which] = self.FF
                    self.curb[which] = 0
                    nSelected += 1

            # Construir textos
            self.ctryStr = ""
            self.nSelectedCountries = nSelected
            if nSelected > 0:
                comProp1 = (1 << 63) - 1
                comProp2 = (1 << 63) - 1
                for i in range(nSelected - 1, -1, -1):
                    which = self.whichSel[i]
                    if 0 <= which < self.nCountries:
                        self.ctryStr += self.countryNames[which] + (", " if i > 0 else " : ")
                        comProp1 &= self.countryProp1[which]
                        comProp2 &= self.countryProp2[which]
                        self.iCh[i] = self.countryNames[which][0]

                # Construir el string del eje
                if self.doText:
                    nCommonProp1 = bin(comProp1).count("1")
                    nCommonProp2 = bin(comProp2).count("1")
                    nProps = nCommonProp1 + nCommonProp2
                    self.axisStr = ""
                    self.axisStr2 = ""

                    if nSelected == 3:
                        initial = all(ch == self.iCh[0] for ch in self.iCh)
                        if nProps > 0:
                            self.axisStr = "Axis of "
                            for b in range(self.nProperties2):
                                if b < 63:
                                    common = comProp1
                                    bit = b
                                else:
                                    common = comProp2
                                    bit = b - 63

                                if (common >> bit) & 1:
                                    prop_name = self.propNames[b]
                                    self.axisStr += prop_name + (", " if nProps > 2 else ".")
                        else:
                            self.axisStr = "Axis of countries." if initial else "These countries have not yet registered their Axis."

                    self.doText = False

            # Actualizar indicadores flotantes (simulado)
            self.filtered = True

    
    def highlight_country_at_cursor(self, x, y):
        self.do_text = True
        self.csr_index = -1
        
        if 0 <= x < self.APP_W and self.IY <= y < self.APP_H:
            self.csr_index = (y - self.IY) * self.IW + x
            if 0 <= self.csr_index < self.NPELS:
                ctry_id = self.src_array[self.csr_index] & 0xFF
                if 0 <= ctry_id < self.n_countries:
                    self.highlites[self.cur_ctry_id := ctry_id] = 0xFF
                    self.lite_str = f"{self.country_names[self.cur_ctry_id]}"
                else:
                    self.lite_str = ""

    def paint(self, screen):
        try:
            self.display_area.fill(self.colb)
            pygame.draw.rect(self.display_area, self.colb, (0, 0, self.APP_W, self.IY))
            
            if self.filtered:
                if self.dst_img:
                    dst_surface = pygame.image.frombuffer(self.dst_img, (self.IW, self.APP_H - self.IY), "RGB")
                    self.display_area.blit(dst_surface, (0, self.IY))
            else:
                pygame.draw.rect(self.display_area, self.colb, (0, 0, self.APP_W, self.APP_H))
            
            pygame.draw.rect(self.display_area, (0, 0, 0), (0, self.IY - 1, self.IW - 1, self.APP_H - self.IY), 1)

            # Dibuja lista de países
            self._draw_text(self.display_area, self.ctry_str, 10, 21, self.ctry_font, 
                            (255, 255, 0) if self.n_selected_countries == 3 else self.colu)
            
            # Dibuja etiquetas de ejes
            self._draw_text(self.display_area, self.axis_str, 10, 37, self.axis_font, (255, 255, 0))
            self._draw_text(self.display_area, self.axis_str2, 10, 53, self.axis_font, (255, 255, 0))

            # Dibuja el indicador flotante
            if self.lite_str and self.csr_y >= self.IY:
                pygame.draw.rect(self.display_area, self.colb, (self.bx, self.by, self.bw, self.bh))
                pygame.draw.rect(self.display_area, (0, 0, 0), (self.bx, self.by, self.bw, self.bh), 1)

                color = (255, 255, 0) if self.cur_ctry_id in self.which_sel else self.colu
                self._draw_text(self.display_area, self.lite_str, self.bx + 6, self.by + self.bh - 5, self.lite_font, color)

            # Blit final a la pantalla
            screen.blit(self.display_area, (0, 0))
            pygame.display.flip()
        except Exception as e:
            print(f"Error during painting: {e}")

    def _draw_text(self, surface, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))


    

if __name__ == "__main__":
    root1 = tk.Tk()
    app1 = CountryHighlighterApp(root1)
    root1.mainloop()
    
    root2 = tk.Tk()
    root2.title("Axis Applet")
    app2 = AxisApplet(root2)
    root2.mainloop()
