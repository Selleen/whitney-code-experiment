'the project consists of three files:

'	main.bas	the main state loop behavior (this file)

' 	const.bas	global constants and graphic resources

'	engine.frm	handles "old school" pixel rendering and window operations



'astute observers will recognize the characters from the annals of gaming history :) 







'the main (emotional) state loop







Sub Main()

  

  The_Story.Show



  While True

    If YourAttitude = CHAUVINIST Then

       

        If Fetch(pail, jack, jill) Then GoUpHill jack, jill

        If FellDown(jack) And BrokeCrown(jack) Then TumblingAfter jill, jack

    

    ElseIf YourAttitude = FEMINIST Then

        

        If Fetch(pail, jill, jack) Then GoUpHill jill, jack

        If FellDown(jill) And BrokeCrown(jill) Then TumblingAfter jack, jill

    

    End If

    The_Story.Draw

  Wend

  

End Sub



Function GoUpHill(Leader As PERSON, follower As PERSON) As Boolean



  If ChangeItIf(SlimChance) Then

    If (Leader.EmotionalState = INDECISIVE Or Leader.EmotionalState = RELUCTANT) And ChangeItIf(Leader.Desire) Then

      Leader.EmotionalState = WILLING

    ElseIf (Leader.EmotionalState = INDECISIVE Or Leader.EmotionalState = WILLING) And ChangeItIf(1 - Leader.Desire) Then

      Leader.EmotionalState = RELUCTANT

    ElseIf (Leader.EmotionalState = RELUCTANT Or Leader.EmotionalState = WILLING) And ChangeItIf(1 - follower.Desire) Then

      Leader.EmotionalState = INDECISIVE

    End If

  End If

  

  If ChangeItIf(follower.Desire) And Leader.EmotionalState <> FALLING Then

    follower.EmotionalState = Leader.EmotionalState

  End If

  If ChangeItIf(SmallChance) Then

    If (follower.EmotionalState = INDECISIVE Or follower.EmotionalState = RELUCTANT) And ChangeItIf(follower.Desire) Then

      follower.EmotionalState = WILLING

    ElseIf (follower.EmotionalState = INDECISIVE Or follower.EmotionalState = WILLING) And ChangeItIf(1 - follower.Desire) Then

      follower.EmotionalState = RELUCTANT

    ElseIf (follower.EmotionalState = RELUCTANT Or follower.EmotionalState = WILLING) And ChangeItIf(1 - Leader.Desire) Then

      Leader.EmotionalState = INDECISIVE

    End If

  End If

  

End Function



Function Fetch(Goal As BUCKET, Leader As PERSON, follower As PERSON) As Boolean



  Static lastFetch As Boolean

  If Leader.EmotionalState = TUMBLING Then

    lastFetch = False

  Else

    If ChangeItIf(SmallChance) Then

      If ChangeItIf(Goal.Allure) Then

        Leader.EmotionalState = WILLING

        follower.EmotionalState = WILLING

        lastFetch = True

      ElseIf ChangeItIf(1 - Goal.Allure) Then

        Leader.EmotionalState = RELUCTANT

        follower.EmotionalState = RELUCTANT

        lastFetch = False

      End If

    End If

  End If

  Fetch = lastFetch



End Function



Function FellDown(Leader As PERSON) As Boolean



  Static lastFell As Boolean  

  If Leader.direction = UpHill And _

  Leader.position.X > TOP_OF_HILL And _

  Leader.EmotionalState = RELUCTANT Then

      lastFell = True

      Leader.EmotionalState = FALLING

  Else

    lastFell = False

  End If

  FellDown = lastFell



End Function



Function BrokeCrown(Leader As PERSON) As Boolean



  Static lastCrown As Boolean

  If Leader.EmotionalState = FALLING Then

    If ChangeItIf(GoodChance) Then

      Leader.EmotionalState = BROKE_CROWN

      lastCrown = True

    End If

  Else

    lastCrown = False

  End If

  BrokeCrown = lastCrown



End Function



Sub TumblingAfter(follower As PERSON, Leader As PERSON)



  If Leader.EmotionalState = BROKE_CROWN Then

    If ChangeItIf(GoodChance) Then

      Leader.EmotionalState = TUMBLING

      follower.EmotionalState = INDECISIVE

    End If

  End If



End Sub



Function ChangeItIf(percent As Single) As Boolean

  If Rnd(1) <= percent Then ChangeItIf = True Else ChangeItIf = False

End Function