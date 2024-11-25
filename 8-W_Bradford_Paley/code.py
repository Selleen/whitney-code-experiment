import tkinter as tk
from tkinter import Canvas


class Line:
    def __init__(self, s):
        self.s = s
        self.leadingPixels = -1
        self.x = 0
        self.y = 0
        self.lineIndex = 0
        self.lineAsWrittenIndex = 0
        self.i1 = None
        self.hasLineCall = False
        self.i2 = None
        self.brightness = 0.0
        self.i17 = None

class Cubic:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def evaluate(self, u):
        return (((self.d * u) + self.c) * u + self.b) * u + self.a
        
class CodeProfiles:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Profiles")
        self.canvas = Canvas(master, bg="black", width=800, height=600)
        self.canvas.pack()
        
        # Placeholder for data structures
        self.programLineIndexAsWritten = [0] * 256
        self.programLineExecutionCount = [0] * 256
        self.programTrace = [0] * 4096
        self.lastLineCallInProgram = 0
        self.programLines = []
        
        # Start visualization
        self.draw_code_profiles()

    

    def draw_code_profiles(self):
        self.canvas.create_text(400, 300, text="Code Profiles Visualization", fill="white", font=("Courier", 16))
        self.canvas.create_oval(100, 100, 110, 110, fill="white")  
        self.canvas.create_oval(200, 200, 210, 210, fill="orange")
        self.canvas.create_oval(300, 300, 310, 310, fill="green") 


    drawnInsertionLine, drawnInsertionLineBackup, drawnInsertionPoint = Line(75)
    drawnFixationLine, drawnFixationPoint, drawnPC = Line(75)
    lineDrawnLarger, lastLineDrawnLarger = None, None
    i14 = Line(117)
    lineDrawnLargerRatio = 1.0 / 3.0
    i25 = Line(244)


    def step():
        global drawnInsertionLine, drawnInsertionLineBackup, drawnInsertionPoint
        global drawnFixationLine, drawnFixationPoint, drawnPC
        global lineDrawnLarger, lastLineDrawnLarger, lineDrawnLargerRatio
        global lineToStartTraces, lineUnderMouseIndex, programLines
        global programLineIndexAsWritten, programTrace, drawnPCWaitTargetLine
        global resetTraceVectors, lastLineCallInProgram

        if lineToStartTraces is not None:
            Line(251)
            drawnFixationPoint = 0
            Line(230)
            drawnFixationLine = lineUnderMouseIndex
            Line(224)
            drawnInsertionPoint = drawnInsertionLineBackup = 0
            Line(232)

            if lineToStartTraces.hasLineCall:
                drawnInsertionLine = lineToStartTraces.lineAsWrittenIndex
                Line(231)
            else:
                i = lineToStartTraces.lineIndex
                Line(235)
                while i != 0 and not programLines[i].hasLineCall:
                    i = (i + 1) % len(programLines)
                    Line(252)
                    drawnInsertionLineBackup -= 1
                    Line(234)
                drawnInsertionLine = lastLineCallInProgram if i == 0 else programLines[i].lineAsWrittenIndex
                Line(233)

            resetTraceVectors = True
            Line(225)
            drawnPCWaitTargetLine = drawnInsertionLine
            Line(236)
            lineToStartTraces = None
            Line(253)

        if lastLineDrawnLarger == lineDrawnLarger:
            Line(246)
            lineDrawnLargerRatio = min(1.0, lineDrawnLargerRatio * 1.05)
        else:
            lineDrawnLargerRatio = 1.0 / 3.0
            Line(247)
            lastLineDrawnLarger = lineDrawnLarger
            Line(245)

        lastLine = programLines[drawnFixationLine]
        Line(206)

        if programLines[drawnFixationLine] is None or drawnFixationPoint >= len(programLines[drawnFixationLine].s) - 1:
            Line(95)
            while True:
                drawnFixationLine = (drawnFixationLine + 1) % len(programLines)
                Line(83)
                if programLines[drawnFixationLine] is not None and programLines[drawnFixationLine].s.strip():
                    break
            Line(98)
            drawnFixationPoint = 0
            Line(96)

        drawnFixationPoint = programLines[drawnFixationLine].s.find(" ", drawnFixationPoint)
        Line(93)
        if "              " in programLines[drawnFixationLine].s[drawnFixationPoint:]:
            drawnFixationPoint += 14
            Line(216)
        if drawnFixationPoint == -1:
            drawnFixationPoint = len(programLines[drawnFixationLine].s) - 2
            Line(94)
        drawnFixationPoint += 1
        Line(97)
        if lineDrawnLarger == lastLine:
            lineDrawnLarger = programLines[drawnFixationLine]
            Line(205)
        lastLine = programLines[programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup]
        Line(210)
        if drawnInsertionPoint + 1 > len(programLines[programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup].s.strip()):
            Line(91)
            if drawnInsertionLineBackup < 0:
                drawnInsertionLineBackup += 1
                Line(106)
            else:
                Line(107)
                while True:
                    drawnInsertionLine = (drawnInsertionLine + 1) % len(programLineIndexAsWritten)
                    Line(84)
                    if programLineIndexAsWritten[drawnInsertionLine] != 0:
                        break
                drawnInsertionLineBackup = 0
                Line(104)
                while (
                    drawnInsertionLine + drawnInsertionLineBackup > 0 and
                    programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup > 0 and
                    not programLines[programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup].s.startswith("//") and
                    not programLines[programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup].hasLineCall
                ):
                    drawnInsertionLineBackup -= 1
                    Line(105)
                drawnInsertionLineBackup += 1
                Line(108)
            drawnInsertionPoint = 0
            Line(92)

        if lineDrawnLarger == lastLine:
            lineDrawnLarger = programLines[programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup]
            Line(209)

        if drawnPCWaitTargetLine == -1:
            lastLine = programLines[programLineIndexAsWritten[programTrace[drawnPC]]]
            Line(207)
            drawnPC = (drawnPC + 1) % len(programTrace)
            Line(74)
            if drawnPC == 0:
                pc = -drawnInsertionLine * 10
                Line(99)
            if lineDrawnLarger == lastLine:
                lineDrawnLarger = programLines[programLineIndexAsWritten[programTrace[drawnPC]]]
                Line(208)
    lastUpdateTime = 0
    i10 = Line(69)

    go = True
    i23 = Line(243)

    lineToStartTraces = None
    i26 = Line(254)

    programLines = None
    lineUnderMouseIndex = -1
    def run():
        global lastUpdateTime, go, programLines

        programLines = readFile(getParameter("fileName")) 
        addMouseMotionListener(lambda e: setLineDrawnLarger(findLineUnderMouse(e))) 
        addMouseListener(
            mousePressed=lambda e: setLineDrawnLarger(findLineUnderMouse(e)), 
            mouseClicked=lambda e: setLineToStartTraces(findLineUnderMouse(e))
        )

        while go:
            step() 
            drawAll(getGraphics())
            try:
                sleepTime = max(0, 15 - (currentMillis() - lastUpdateTime))
                time.sleep(sleepTime / 1000.0) 
                Line(70)
            except Exception as e:
                print(e)

            lastUpdateTime = currentMillis()
    def findLineUnderMouse(e):
        global lineUnderMouseIndex

        lineUnderMouse = None
        lineUnderMouseIndex = -1 

        for i in range(len(programLines)):
            if (
                e.getX() > (programLines[i].x - programLines[i].leadingPixels) and
                e.getX() < (programLines[i].x - programLines[i].leadingPixels + columnWidth) and
                e.getY() > programLines[i].y - 3 and
                e.getY() < programLines[i].y
            ):
                lineUnderMouse = programLines[i]
                lineUnderMouseIndex = i
                break

        Line(115)
        return lineUnderMouse

    def addMouseMotionListener(onMouseMoved):
        pass

    def addMouseListener(mousePressed=None, mouseClicked=None):
        pass

    def setLineDrawnLarger(lineDrawn):
        pass

    def setLineToStartTraces(lineToStart):
        global lineToStartTraces
        lineToStartTraces = lineToStart

    def readFile(filename):
        pass

    def getParameter(paramName):
        pass

    def step():
        pass

    def drawAll(graphics):
        pass

    def getGraphics():
        pass

    def currentMillis():
        import time
        return int(time.time() * 1000)

    def Line(lineNumber):
        pass
        
    pc = 0
    drawnPCWaitTargetLine = -1
    i5 = Line(38)

    buffer = bytearray(1000)
    i3 = Line(31)

    def Line(i, recur=False):
        global pc, drawnPCWaitTargetLine

        if recur:
            Line(3)

        if drawnPCWaitTargetLine == i:
            drawnPC = pc = 0
            if recur:
                Line(237)

            drawnPCWaitTargetLine = -1
            if recur:
                Line(240)

        if programTrace is not None and pc < len(programTrace) and drawnPCWaitTargetLine == -1:
            programTrace[max(0, min(pc, len(programTrace) - 1))] = i
            pc += 1

        if recur:
            Line(39)

        if programLineExecutionCount is not None:
            programLineExecutionCount[i] += 1
            if recur:
                Line(133)

        return i
    
    def brightenExecutedLines(g, all):
        Line(135)
        for i in range(len(programLineIndexAsWritten)):
            Line(140)
            newBrightness = math.log(programLineExecutionCount[i] + 1)
            Line(141)
            if all or (programLines is not None and 
                       abs(newBrightness - programLines[programLineIndexAsWritten[i]].brightness) > 0.4) and \
                    programLineIndexAsWritten[i] != 0:
                Line(143)
                index = programLineIndexAsWritten[i]
                backup = 0
                Line(137)
                programLines[index].brightness = newBrightness
                Line(142)
                greenComponent = int(min(150, 70 + programLines[index].brightness * 2))
                Line(149)
                g.setColor((greenComponent // 3, greenComponent, greenComponent // 3))
                Line(136)
                if programLines is not None and programLines[index] is not None:
                    while index + backup > 0 and \
                            programLines[index + backup].s.find("//") != 0 and \
                            not programLines[index + backup].hasLineCall:
                        g.drawString(
                            programLines[index + backup].s,
                            programLines[index + backup].x,
                            programLines[index + backup].y
                        )
                        Line(138)
                        backup -= 1
                    Line(139)

    def readFile(fileName):
        Line(4)
        v = []
        Line(10)

        try:
            Line(7)
            url = getCodeBase() + fileName
            is_ = urlopen(url)
            Line(5)
            br = is_.readlines()
            Line(19)
            l = None
            Line(12)
            for Line in br:
                l = readLine(Line.decode('utf-8').strip())
                Line(9)
                if l is not None:
                    v.append(l)
                Line(11)
            Line(14)

            is_.close()
            Line(6)

        except Exception as e:
            print(e)
            Line(8)
            
        lines = [None] * len(v)
        Line(33)
        for i in range(len(v)):
            lines[i] = v[i]
            Line(48)
            lines[i].lineIndex = i
            lineCallPos = lines[i].s.find("Line(")
            lineCallEndPos = lines[i].s.find(")", lineCallPos)
            Line(85)
            Line(82)

            if lineCallPos != -1 and lines[i].s[lineCallEndPos - 1].isdigit():
                lines[i].hasLineCall = True
                Line(103)

                programLineIndexAsWritten[lastLineCallInProgram] = i
                lines[i].lineAsWrittenIndex = int(lines[i].s[lineCallPos + 5:lineCallEndPos])
                Line(81)

        return lines

    def readLine(br):
        Line(15)

        length = 0
        Line(20)
        ch = None
        Line(21)

        try:
            Line(22)
            for ch in br:
                if ch in ('\n', '\r', -1):
                    break
                buffer[length] = ord(ch)
                length += 1
                Line(23)
            if ch == -1:
                return None
            Line(24)
            if ch == '\r':
                Line(25)

            Line(27)

        except Exception:
            return None
            Line(28)

        if length == 0:
            return Line("")
        Line(29)

        return Line("".join(chr(buffer[i]) for i in range(length)) + " ")
        Line(30)

    from PIL import Image, ImageDraw, ImageFont
    from collections import deque
    from typing import List

    cache_image = None
    offscreen_image = None
    i7 = Line(54)

    cacheGraphics = None
    offscreenGraphics = None
    i8 = Line(55)

    drawCacheNeeded = True
    resetTraceVectors = False
    i9 = Line(62)

    pastPCPositions = deque()
    i13 = Line(109)
    pastFixationPositions = deque()
    i18 = Line(177)
    pastInsertionPositions = deque()
    i19 = Line(184)

    last_fixation_line = None
    i21 = Line(200)

    last_insertion_line = None
    i20 = Line(197)


    def draw_all(g):
        global offscreen_image, cache_image, offscreenGraphics, cacheGraphics
        global drawCacheNeeded, resetTraceVectors, pastPCPositions, pastFixationPositions, pastInsertionPositions

        Line(53)

        if getSize().width < 21 or getSize().height < 21:
            Line(255)
            return

        if (
            offscreen_image is None
            or getSize().width != offscreen_image.width
            or getSize().height != offscreen_image.height
        ):
            Line(56)
            setFont(Font("Courier", Font.PLAIN, max(1, getSize().width // 320)))
            Line(78)
            offscreen_image = createImage(getSize().width, getSize().height)
            Line(57)
            offscreenGraphics = ImageDraw.Draw(offscreen_image)
            Line(58)
            resetTraceVectors = True
            Line(228)

        if (
            cache_image is None
            or getSize().width != cache_image.width
            or getSize().height != cache_image.height
        ):
            Line(59)
            cache_image = createImage(getSize().width, getSize().height)
            Line(60)
            cacheGraphics = ImageDraw.Draw(cache_image)
            Line(61)
            drawCacheNeeded = True
            Line(63)

        if cacheGraphics is None or offscreenGraphics is None:
            Line(131)
            return

        if drawCacheNeeded:
            drawCache(cacheGraphics)
            Line(66)

        if programLines:
            brightenExecutedLines(cacheGraphics, False)
            Line(144)


        offscreenGraphics.bitmap((0, 0), cache_image, fill=None)
        Line(67)

        if resetTraceVectors:
            Line(229)
            pastPCPositions = deque()
            Line(217)
            pastFixationPositions = deque()
            Line(218)
            pastInsertionPositions = deque()
            Line(219)
            resetTraceVectors = False

        drawFixationTrace(g)
        drawInsertionTrace(g)
        drawExecutionTrace(g)

        line_recently_drawn_larger = lineDrawnLarger
        Line(124)
        if line_recently_drawn_larger:
            Line(121)
            offscreenGraphics.set_color((30, 255, 30))
            Line(120)
            offscreenGraphics.setFont(Font(getFont().getName(), getFont().get_style(), 12))
            Line(122)
            offscreenGraphics.text(
                (min(
                    getSize().width - lineDrawnLargerRatio * getFontMetrics(offscreenGraphics.getFont()).string_width(line_recently_drawn_larger.s.strip()),
                    line_recently_drawn_larger.x
                ), line_recently_drawn_larger.y),
                line_recently_drawn_larger.s
            )
            Line(123)
            offscreenGraphics.setFont(getFont())
            Line(125)

        offscreenGraphics.set_color((0, 255, 0))
        Line(85)

        index = programLineIndexAsWritten[programTrace[drawnPC]]
        backup = 0
        Line(100)

        if drawnPCWaitTargetLine == -1 and programTrace[drawnPC] != 0 and programLines and programLines[index]:
            while True:
                offscreenGraphics.text(
                    (programLines[index + backup].x, programLines[index + backup].y),
                    programLines[index + backup].s
                )
                Line(86)
                if programLines[index + backup].s.strip() and programLines[index + backup].y > 1 and drawnPC < pc:
                    pastPCPositions.insert(
                        0,
                        Point(programLines[index + backup - 1].x, programLines[index + backup - 1].y)
                    )
                Line(110)
                backup -= 1
                if not (index + backup > 0 and "//" not in programLines[index + backup].s and not programLines[index + backup].has_line_call):
                    break
                
            Line(102)


    # --------------------------------------------------------------------------
    # draw the fixation point
    if programLines is not None:
        offscreenGraphics.setColor((255, 255 * 7 // 8, 0))

        # if it's the attended Line draw it larger and brighter
        if lineRecentlyDrawnLarger == programLines[drawnFixationLine]:
            offscreenGraphics.setFont((getFont().getName(), getFont().getStyle(), 12))

        offscreenGraphics.drawString(
            programLines[drawnFixationLine].s[:drawnFixationPoint],
            int(min(
                getSize().width - lineDrawnLargerRatio *
                getFontMetrics(offscreenGraphics.getFont()).stringWidth(
                    programLines[drawnFixationLine].s.strip()
                ),
                programLines[drawnFixationLine].x
            )),
            programLines[drawnFixationLine].y
        )

        # remember the position if it's not a blank Line
        if (
            lastFixationLine is None or
            lastFixationLine != programLines[drawnFixationLine] and
            len(programLines[drawnFixationLine].s.strip()) != 0 and
            programLines[drawnFixationLine].y > 1
        ):
            pastFixationPositions.append((
                programLines[drawnFixationLine].x +
                getFontMetrics(getFont()).stringWidth(
                    programLines[drawnFixationLine].s.strip()
                ),
                programLines[drawnFixationLine].y
            ))
            pastFixationPositions.append((
                programLines[drawnFixationLine].x,
                programLines[drawnFixationLine].y
            ))

        lastFixationLine = programLines[drawnFixationLine]

        # if it's the Line drawn larger put the font back to normal
        if lineRecentlyDrawnLarger == programLines[drawnFixationLine]:
            offscreenGraphics.setFont(getFont())

    # --------------------------------------------------------------------------
    # draw the insertion point
    offscreenGraphics.setColor((255, 255, 255))

    if programLineIndexAsWritten[drawnInsertionLine] != 0:
        insertionLine = programLines[
            programLineIndexAsWritten[drawnInsertionLine] + drawnInsertionLineBackup
        ]

        # if it's the attended Line draw it larger and brighter
        if lineRecentlyDrawnLarger == insertionLine:
            offscreenGraphics.setFont((getFont().getName(), getFont().getStyle(), 12))

        offscreenGraphics.drawString(
            insertionLine.s[:drawnInsertionPoint],
            int(min(
                getSize().width - lineDrawnLargerRatio *
                getFontMetrics(offscreenGraphics.getFont()).stringWidth(
                    insertionLine.s.strip()
                ),
                insertionLine.x
            )),
            insertionLine.y
        )

        # remember the position if it's not a blank Line
        if (
            lastInsertionLine is None or
            lastInsertionLine != insertionLine and
            len(insertionLine.s.strip()) != 0 and
            insertionLine.y > 1
        ):
            pastInsertionPositions.append((insertionLine.x, insertionLine.y))
            pastInsertionPositions.append((
                insertionLine.x +
                getFontMetrics(getFont()).stringWidth(insertionLine.s.strip()),
                insertionLine.y
            ))

        lastInsertionLine = insertionLine

        # if it's the Line drawn larger put the font back to normal
        if lineRecentlyDrawnLarger == insertionLine:
            offscreenGraphics.setFont(getFont())

    # --------------------------------------------------------------------------
    # copy the graphics cache into the back buffer
    g.drawImage(offscreenImage, 0, 0)

    # ==============================================================================
    def drawExecutionTrace(g):
        global pastPCPositions

        # if we just started a new sample of trace, start a new trace Line
        if drawnPC == 0:
            pastPCPositions = []

        # trim the Line to trace only the last 200 PC positions
        while len(pastPCPositions) > 200:
            pastPCPositions.pop(0)

        # draw from the tail forward
        for i in range(1, len(pastPCPositions)):
            # fade it out slowly
            lineBrightness = min(
                140,
                20 + i + max(0, 200 - len(pastPCPositions))
            )

            offscreenGraphics.setColor((
                lineBrightness // 8,
                lineBrightness,
                lineBrightness // 8
            ))

            offscreenGraphics.drawLine(
                pastPCPositions[i - 1].x, pastPCPositions[i - 1].y,
                pastPCPositions[i].x, pastPCPositions[i].y
            )

    
    # ==============================================================================

    def drawInsertionTrace(g):
        global pastInsertionPositions
    
        # trim the Line to trace only the last 30 insertion positions
        while len(pastInsertionPositions) > 30:
            pastInsertionPositions.pop(0)  # Line(186)
    
        if len(pastInsertionPositions) > 1:  # Line(187)
            insertionSpline = calculateNaturalCubic(pastInsertionPositions)  # Line(188)
    
            insertionLine = programLines[programLineIndexAsWritten[
                drawnInsertionLine] + drawnInsertionLineBackup]  # Line(212)
    
            lastStepRatio = (
                1.0 if len(insertionLine.s.strip()) == 0
                else drawnInsertionPoint / len(insertionLine.s.strip())
            )  # Line(213)
    
            # draw from the tail forward
            steps = 40  # Line(189)
            for i in range(len(insertionSpline) -
                           (2 if lastStepRatio < 0.5 and lastStepRatio != 0.0 else 1)):
                
                # fade it out slowly
                lineBrightness = min(140, 20 + i * 5 +
                                     max(0, 30 - len(insertionSpline)) * 5)  # Line(204)
                offscreenGraphics.setColor((lineBrightness, lineBrightness, lineBrightness))
    
                # figure out where to stop
                lastStep = int(steps)  # Line(214)
                if lastStepRatio < 0.5 and lastStepRatio != 0.0 and i == len(insertionSpline) - 3:
                    lastStep = int(lastStepRatio * 2 * steps)
                elif lastStepRatio >= 0.5 and i == len(insertionSpline) - 2:
                    lastStep = int((lastStepRatio - 0.5) * 2 * steps)  # Line(215)
    
                # do the drawing
                p1 = (
                    round(insertionSpline[i][0].evaluate(0)),
                    round(insertionSpline[i][1].evaluate(0))
                )  # Line(194)
    
                for j in range(1, lastStep + 1):
                    p2 = (
                        round(insertionSpline[i][0].evaluate(j / steps)),
                        round(insertionSpline[i][1].evaluate(j / steps))
                    )  # Line(195)
                    if p1 is not None:
                        offscreenGraphics.drawLine(p1[0], p1[1], p2[0], p2[1])  # Line(190)
                    p1 = p2  # Line(196)
    
    # ==============================================================================
    
    def drawFixationTrace(g):
        global pastFixationPositions
    
        
        while len(pastFixationPositions) > 80:
            pastFixationPositions.pop(0) 
    
        if len(pastFixationPositions) > 1: 
            fixationSpline = calculateNaturalCubic(pastFixationPositions) 
    
            # draw from the tail forward
            for i in range(len(fixationSpline) - 1):
            
                # fade it out slowly
                lineBrightness = min(120, 20 + int(i * 1.5) +
                                     max(0, 80 - len(fixationSpline)) * 2)  # Line(203)
                offscreenGraphics.setColor((
                    lineBrightness, lineBrightness * 7 // 8, lineBrightness // 4))
    
                steps = 13  # Line(157)
                p1 = (
                    round(fixationSpline[i][0].evaluate(0)),
                    round(fixationSpline[i][1].evaluate(0))
                )  # Line(191)
    
                for j in range(1, int(steps) + 1):
                    p2 = (
                        round(fixationSpline[i][0].evaluate(j / steps)),
                        round(fixationSpline[i][1].evaluate(j / steps))
                    )  # Line(192)
                    if p1 is not None:
                        offscreenGraphics.drawLine(p1[0], p1[1], p2[0], p2[1])  # Line(181)
                    p1 = p2  # Line(193)

    
        #==============================================================================

    def drawCache(g):
        # start with a "no-electron CRT" black background
        g.set_color("black")  # Cambiado a una representación genérica
        g.fill_rect(0, 0, get_size().width, get_size().height)

        if programLines is not None and cacheImage.get_height(self) != 0:
            drawCode(g, cacheImage.get_width(self), cacheImage.get_height(self))
            # we drew it
            drawCacheNeeded = False


    #==============================================================================
    columnWidth = 0
    i27 = Line(249)

    def drawCode(g, w, h):
        columns = 4
        linesPerCol = (len(programLines) + columns - 1) // columns
        margin = w // 8
        colSpacing = columnWidth = (
            (w - margin * 2 - getFontMetrics(g.get_font()).string_width(" ") * 100)
            // (columns - 1)
        )
        lineHeight = (h - margin * 2) / (linesPerCol + 2)

        # draw the code in "early CRT phosphor" green
        g.set_color((20, 80, 20))

        # draw every Line of the code we have read
        for i, Line in enumerate(programLines):
            if Line is not None:
                # trim leading spaces the first time we draw the Line
                if Line.leadingPixels == -1:
                    Line.leadingPixels = (
                        Line.s.index(Line.s.strip()) * getFontMetrics(g.get_font()).string_width(" ")
                    )
                    Line.s = Line.s.strip() + "             "

                Line.x = margin + Line.leadingPixels + (i // linesPerCol) * colSpacing
                Line.y = margin + int((i % linesPerCol) * lineHeight)
                g.draw_string(Line.s, Line.x, Line.y)

        brightenExecutedLines(g, True)


    thread = None
    i4 = Line(34)

    def start():
        global thread
        thread = threading.Thread(target=run)
        thread.start()

    def stop():
        global go
        go = False

    def update(g):
        paint(g)

    def paint(g):
        drawAll(g)

    def calculateNaturalCubic(v):
        n = len(v) - 1
        gammas = [0] * (n + 1)
        deltaXs = [0] * (n + 1)
        DXs = [0] * (n + 1)
        deltaYs = [0] * (n + 1)
        DYs = [0] * (n + 1)

        # gammas
        gammas[0] = 1 / 2.0
        for i in range(1, n):
            gammas[i] = 1 / (4 - gammas[i - 1])
        gammas[n] = 1 / (2 - gammas[n - 1])

        # deltas for x
        deltaXs[0] = 3 * (v[1].x - v[0].x) * gammas[0]
        for i in range(1, n):
            deltaXs[i] = (3 * (v[i + 1].x - v[i - 1].x) - deltaXs[i - 1]) * gammas[i]
        deltaXs[n] = (3 * (v[n].x - v[n - 1].x) - deltaXs[n - 1]) * gammas[n]

        # Ds for x
        DXs[n] = deltaXs[n]
        for i in range(n - 1, -1, -1):
            DXs[i] = deltaXs[i] - gammas[i] * DXs[i + 1]

        # deltas for y
        deltaYs[0] = 3 * (v[1].y - v[0].y) * gammas[0]
        for i in range(1, n):
            deltaYs[i] = (3 * (v[i + 1].y - v[i - 1].y) - deltaYs[i - 1]) * gammas[i]
        deltaYs[n] = (3 * (v[n].y - v[n - 1].y) - deltaYs[n - 1]) * gammas[n]

        # Ds for y
        DYs[n] = deltaYs[n]
        for i in range(n - 1, -1, -1):
            DYs[i] = deltaYs[i] - gammas[i] * DYs[i + 1]

        # coefficients of the cubics
        coefficients = [[None, None] for _ in range(n)]
        for i in range(n):
            coefficients[i][0] = Cubic(
                v[i].x,
                DXs[i],
                3 * (v[i + 1].x - v[i].x) - 2 * DXs[i] - DXs[i + 1],
                2 * (v[i].x - v[i + 1].x) + DXs[i] + DXs[i + 1],
            )
            coefficients[i][1] = Cubic(
                v[i].y,
                DYs[i],
                3 * (v[i + 1].y - v[i].y) - 2 * DYs[i] - DYs[i + 1],
                2 * (v[i].y - v[i + 1].y) + DYs[i] + DYs[i + 1],
            )

        return coefficients

  

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeProfiles(root)
    root.mainloop()
