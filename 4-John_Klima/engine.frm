
'the graphics "engine" of sorts, including the window specific handlers


Private Declare Function timeGetTime& Lib "winmm.dll" ()

Dim jackImg(4, 15, 15)

Dim jillImg(4, 14, 21)

Dim pailImg(1, 15, 15)

Dim hillImg(1, 15, 7)



Public Sub Draw()

  'uses global jack and jill

  Select Case jack.EmotionalState

    Case INDECISIVE

      PauseTheHill jack

    Case WILLING

      MoveUpTheHill jack, jill

    Case RELUCTANT

      MoveDownTheHill jack, jill

    Case FALLING

      FellDown jack

    Case BROKE_CROWN

      BrokeCrown jack

    Case TUMBLING

      TumblingThem jack, jill

  End Select



  Select Case jill.EmotionalState

    Case INDECISIVE

      PauseTheHill jill

    Case WILLING

      MoveUpTheHill jill, jack

    Case RELUCTANT

      MoveDownTheHill jill, jack

    Case FALLING

      FellDown jill

    Case BROKE_CROWN

      BrokeCrown jill

    Case TUMBLING

      TumblingThem jill, jack

  End Select

  

  Dim Graphic As Variant

  Dim pos As VECTOR

  Static Frame As Integer

  Static fc As Long

  Dim d As Long

  Dim t As Integer

  

  d = timeGetTime()

  drawSprite jackImg, jack.position, jack.Frame, jack.direction, jack.orientation

  drawSprite jillImg, jill.position, jill.Frame, jill.direction, jill.orientation

  

  The_Picture.Picture = buffer.Image

  

  t = CInt(Abs(timeGetTime() - d))

  fc = fc + t

  If fc > 100 Then

    fc = 0

    eraseSprite jackImg, jack.position, jack.Frame, jack.direction, jack.orientation

    eraseSprite jillImg, jill.position, jill.Frame, jill.direction, jill.orientation

    jack.Frame = jack.Frame + 1

    If jack.Frame > 1 Then jack.Frame = 0

    jill.Frame = jill.Frame + 1

    If jill.Frame > 1 Then jill.Frame = 0

  End If

  DoEvents

End Sub

Private Sub MoveUpTheHill(A As PERSON, B As PERSON)

  eraseSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

  A.orientation = 0

  

  Dim collide As Integer

  If B.position.X > A.position.X Then

    collide = Abs(A.position.X + 6 - B.position.X + 6)

  Else

    collide = 100

  End If

  

  If A.position.X + 6 < 700 And collide > 16 Then

    A.position.X = A.position.X + 6

    A.direction = 1

    calculateY A

  Else

    A.Frame = 2

  End If

  

End Sub

Private Sub PauseTheHill(A As PERSON)

 eraseSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

 A.Frame = 2

End Sub

Private Sub MoveDownTheHill(A As PERSON, B As PERSON)

  eraseSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

  A.orientation = 0

  Dim collide As Integer

  If B.position.X < A.position.X Then

    collide = Abs(A.position.X - 6 - B.position.X - 6)

  Else

    collide = 100

  End If

  If A.position.X - 6 > 30 And Abs(collide) > 16 Then

    A.position.X = A.position.X - 6

    A.direction = 0

    calculateY A

  Else

    A.Frame = 2

  End If

End Sub



Private Sub FellDown(A As PERSON)

  eraseSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

  A.orientation = 3

  A.Frame = 3

  drawSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

End Sub

Private Sub BrokeCrown(A As PERSON)

  eraseSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

  A.orientation = 3

  A.Frame = 4

  drawSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

End Sub

Private Sub TumblingThem(A As PERSON, B As PERSON)

  eraseSprite A.Graphic, A.position, A.Frame, A.direction, A.orientation

  A.orientation = A.orientation + 1

  If A.orientation > 3 Then A.orientation = 0

  Dim collide As Integer

  

  If B.position.X < A.position.X Then

    collide = Abs(A.position.X - 6 - B.position.X - 6)

  Else

    collide = 100

  End If

  

  If A.position.X - 6 > 30 And Abs(collide) > 16 Then

    A.position.X = A.position.X - 6

    A.direction = 0

    calculateY A

  Else  'they crashed so B tumbles too

    A.position.X = A.position.X - 6

    A.direction = 0

    calculateY A

    eraseSprite B.Graphic, B.position, B.Frame, B.direction, B.orientation

    B.EmotionalState = A.EmotionalState

    B.Frame = 4

    If A.position.X < 0 Then

      reset

    End If

  End If



End Sub

Private Sub drawHill()



  Dim sx As Integer

  Dim sy As Integer

  Dim X As Integer

  Dim Y As Integer

  Dim w As Integer

  Dim h As Integer

  Dim i As Integer

  Dim pos As VECTOR

  

  buffer.DrawWidth = 2

  

  w = UBound(hillImg, 2)

  h = UBound(hillImg, 3)

  sx = 0

  sy = 300 - h * 4 'bottom to top

  For X = w * 2 To 800 - (w * 4) Step (w * 2) + 2

    sy = sy - 4

    pos.X = X: pos.Y = sy

    drawSprite hillImg, pos, 0, 1, 0

  Next X

  'draw the pail

  pos.Y = pos.Y - h * 2 - 3 'on top of last hill primitive

  drawSprite pailImg, pos, 0, 1, 0

  

End Sub



Private Sub drawSprite(Graphic As Variant, pos As VECTOR, Frame As Integer, dirc As Integer, ori As Integer)

 

  Dim X As Integer

  Dim Y As Integer

  Dim w As Integer

  Dim h As Integer

  Dim xp As Integer

  Dim yp As Integer

  Dim clr As Long

  

  If ori = 1 Or ori = 3 Then

    w = UBound(Graphic, 3) * 2

    h = UBound(Graphic, 2) * 2

  Else

    w = UBound(Graphic, 2) * 2

    h = UBound(Graphic, 3) * 2

  End If

  

  For Y = 0 To h Step 2

    For X = 0 To w Step 2

      If ori = 1 Or ori = 3 Then

        clr = Graphic(Frame, Y / 2, X / 2)

      Else

        clr = Graphic(Frame, X / 2, Y / 2)

      End If

      If clr > 0 Then

          If dirc > 0 Then

            xp = pos.X + X

          Else

            xp = pos.X + w - X

          End If

          

          Select Case ori

            Case 0

              yp = pos.Y - h + Y

              buffer.PSet (xp, yp), clr

            Case 1

              yp = pos.Y - h + Y

              buffer.PSet (xp, yp), clr

            Case 2

              yp = pos.Y - Y

              buffer.PSet (xp, yp), clr

            Case 3

              yp = pos.Y - Y

              buffer.PSet (xp, yp), clr

          End Select

        End If

    Next X

  Next Y

  

End Sub



Private Sub eraseSprite(Graphic As Variant, pos As VECTOR, Frame As Integer, dirc As Integer, ori As Integer)

 

  Dim X As Integer

  Dim Y As Integer

  Dim w As Integer

  Dim h As Integer

  Dim xp As Integer

  Dim yp As Integer

  Dim clr As Long

  

  If ori = 1 Or ori = 3 Then

    w = UBound(Graphic, 3) * 2

    h = UBound(Graphic, 2) * 2

  Else

    w = UBound(Graphic, 2) * 2

    h = UBound(Graphic, 3) * 2

  End If

  

  For Y = 0 To h Step 2

    For X = 0 To w Step 2

      If ori = 1 Or ori = 3 Then

        clr = Graphic(Frame, Y / 2, X / 2)

      Else

        clr = Graphic(Frame, X / 2, Y / 2)

      End If

        If clr > 0 Then

          If dirc > 0 Then

            xp = pos.X + X

          Else

            xp = pos.X + w - X

          End If

          Select Case ori

            Case 0

              yp = pos.Y - h + Y

              buffer.PSet (xp, yp), 0

            Case 1

              yp = pos.Y - h + Y

              buffer.PSet (xp, yp), 0

            Case 2

              yp = pos.Y - Y

              buffer.PSet (xp, yp), 0

            Case 3

              yp = pos.Y - Y

              buffer.PSet (xp, yp), 0

          End Select

        End If

    Next X

  Next Y

  

End Sub

Private Sub reset()

  jack.EmotionalState = INDECISIVE

  jill.EmotionalState = INDECISIVE

  SetOptions

  If YourAttitude = CHAUVINIST Then

    PlaceJackAndJill jack, jill

  Else

    PlaceJackAndJill jill, jack

  End If

End Sub



Private Sub PlaceJackAndJill(lead As PERSON, follow As PERSON)

  

  lead.direction = 1

  lead.orientation = 0

  lead.width = UBound(lead.Graphic, 2) * 2

  lead.position.X = 68

  calculateY lead

  

  follow.direction = 1

  follow.orientation = 0

  follow.width = UBound(follow.Graphic, 2) * 2

  follow.position.X = 32

  calculateY follow

  

  buffer.Cls

  drawHill

  

End Sub

Private Sub calculateY(targ As PERSON)

  'y is *ALWAYS* a function of x

  Dim fw As Single

  fw = targ.position.X + targ.width

  targ.position.Y = 254 - 4 * Fix((fw - fw Mod 32) / 32)

End Sub



Private Sub Form_Unload(Cancel As Integer)

  End

End Sub

Sub SetOptions()

  Attitude(0).Value = True

  JillsDesire(1).Value = True

  JacksDesire(1).Value = True

  Allure(1) = True

End Sub

Private Sub Attitude_Click(Index As Integer)

  If Index = 0 Then

    PlaceJackAndJill jack, jill

    YourAttitude = CHAUVINIST

  Else

    PlaceJackAndJill jill, jack

    YourAttitude = FEMINIST

  End If

End Sub

Private Sub JacksDesire_Click(Index As Integer)

  Select Case Index

    Case 0

      jack.Desire = 0

    Case 1

      jack.Desire = 0.5

    Case 2

      jack.Desire = 1

  End Select

End Sub



Private Sub JillsDesire_Click(Index As Integer)

  Select Case Index

    Case 0

      jill.Desire = 0

    Case 1

      jill.Desire = 0.5

    Case 2

      jill.Desire = 1

  End Select

End Sub



Private Sub Allure_Click(Index As Integer)

  Select Case Index

    Case 0

      pail.Allure = 0

    Case 1

      pail.Allure = 0.5

    Case 2

      pail.Allure = 1

  End Select

End Sub



Private Sub Form_Load()

  Randomize Timer

  placeWindow

  

  'translate the image strings into arrays of color values

  ParseImage jack1, jackImg, 0

  ParseImage jack2, jackImg, 1

  ParseImage jack3, jackImg, 2

  ParseImage jack4, jackImg, 3

  ParseImage jack5, jackImg, 4

  

  ParseImage jill1, jillImg, 0

  ParseImage jill2, jillImg, 1

  ParseImage jill3, jillImg, 2

  ParseImage jill4, jillImg, 3

  ParseImage jill5, jillImg, 4

  ParseImage pail1, pailImg, 0

  ParseImage hill, hillImg, 0

    

  jack.Graphic = jackImg

  jill.Graphic = jillImg

  pail.Graphic = pailImg

    

  SetOptions

  

End Sub



Sub ParseImage(ttext As Variant, tarray As Variant, ti As Integer)

  Dim X As Integer

  Dim Y As Integer

  Dim w As Integer

  Dim h As Integer

  Dim t As String

  Dim v As String

  Dim out As String

  w = UBound(tarray, 2)

  h = UBound(tarray, 3)

  For Y = 0 To h

    For X = 0 To w

      v = Mid(ttext, (w + 1) * Y + X + 1, 1)

      tarray(ti, X, Y) = FindColorValue(v)

    Next X

  Next Y

End Sub



Function FindColorValue(tv As String) As Long

  Select Case tv

    Case "O"

      FindColorValue = Ov

    Case "A"

      FindColorValue = Av

    Case "B"

      FindColorValue = Bv

    Case "C"

      FindColorValue = Cv

    Case "D"

      FindColorValue = Dv

    Case "E"

      FindColorValue = Ev

    Case "F"

      FindColorValue = Fv

    Case "G"

      FindColorValue = Gv

    Case "H"

      FindColorValue = Hv

    Case "I"

       FindColorValue = Iv

    Case "J"

      FindColorValue = Jv

  End Select

End Function



Private Sub placeWindow()

  'position the window

  Me.width = 800 * Screen.TwipsPerPixelX

  Me.height = 600 * Screen.TwipsPerPixelY

  Me.Top = (Screen.height - Me.height) / 2

  Me.Left = (Screen.width - Me.width) / 2

  The_Picture.Top = 0

  The_Picture.Left = 0

  The_Picture.width = 800

  The_Picture.height = 600

  buffer.Top = 0

  buffer.Left = 0

  buffer.width = 800

  buffer.height = 600

End Sub