Sub DB_CONNECT()
    Dim x As New ADODB.Connection
    Dim ds As New ADODB.Recordset
    
    
    If x Is Nothing Then
      Set x = CreateObject("adodb.connection")
      x.Open "", "", ""      'MySQL是在ODBC中Data source Name ;root是用户名 123456 是密码，需要提前配置，否则无法连接。
    ElseIf x.State = 0 Then
      Set x = CreateObject("adodb.connection")
      x.Open "", "", ""
    End If
    
    Dim date1 As String
    Dim date2 As String
    date1 = Sheets("jingjia2").Cells(3, "C").value
    date2 = Sheets("jingjia2").Cells(3, "D").value
    date3 = Sheets("jingjia2").Cells(3, "E").value

    Sql = "" 'sql语句

    
    With ds
        .Open Sql, x
        'MsgBox (Sql)
        
        Sheets("Sheet1").Select
        Sheets("Sheet1").Cells.Clear
        
        Dim s As String
        
        ' Range("A2").Cells.Value = 123
        Range("A1").CopyFromRecordset ds '将结果可以放到单元格内
        
    End With
    
    Call isExistSheet

    Sheets("jingjia2").Select
    Sheets("jingjia2").Range("D6:L9").ClearContents
    
   With Sheets("jingjia2")
    Dim i As Integer
    Range("C5").value = ""
    Range("C6").value = ""
    Range("C7").value = ""
    Range("C8").value = ""
    Range("C9").value = ""
    Range("C10").value = ""
    Range("M5").value = ""
    Range("N5").value = ""
    
    Range("D5").value = "0.4"
    Range("E5").value = "0.45"
    Range("F5").value = "0.5"
    Range("G5").value = "0.55"
    Range("H5").value = "0.6"
    Range("I5").value = "0.65"
    Range("J5").value = "0.7"
    Range("K5").value = "0.8"
    Range("L5").value = "1"
    

    Range("C5:M5").Interior.ColorIndex = 37
    Range("C10:L10").Interior.ColorIndex = 37
    Range("N5").Interior.ColorIndex = 46
    Range("N7").Interior.ColorIndex = 46
    Range("M9").Interior.ColorIndex = 46
    
    Range("C5:M5").Font.Bold = True
    Range("C10:L10").Font.Bold = True
    Range("C17:J17").Font.Bold = True
    Range("C18:J18").Font.Bold = True
    Range("C25:J25").Font.Bold = True
    Range("C27:J27").Font.Bold = True
    Range("C28:J28").Font.Bold = True
    Range("C35:J35").Font.Bold = True

    
   End With
    
    
    Call calcPrice '计算总计及占比

   
    Call calculateAIJIA
End Sub


Sub isExistSheet() '是否存在jingjia2表
    Dim x As Integer
    For x = 1 To Sheets.Count
        If Sheets(x).Name = "jingjia2" Then
            'MsgBox "exist"
        Exit Sub
        End If
    Next x
        Sheets.Add
        ActiveSheet.Name = "Sheet4"
        
   For x = 1 To Sheets.Count
        If Sheets(x).Name = "Sheet3" Then
            'MsgBox "exist"
        Exit Sub
        End If
    Next x
        Sheets.Add
        ActiveSheet.Name = "Sheet3"
        
        
End Sub

Sub calcPrice()
With Sheets("sheet1")
    Dim column As Integer
    Dim row As Integer
    Dim total As Integer
    
    Dim value As Single
    Dim t4 As Integer
    Dim t45 As Integer
    Dim t5 As Integer
    Dim t55 As Integer
    Dim t6 As Integer
    Dim t65 As Integer
    Dim t7 As Integer
    Dim t8 As Integer
    Dim t1 As Integer
    
    
    Sheets("jingjia2").Range("D6:L8").ClearContents '防止每次累加，每次进来先清空
    
    column = .UsedRange.Columns.Count '行
    row = .UsedRange.Rows.Count '列
    
    Dim i As Integer
    For i = 1 To row
    
        value = .Cells(i, 6).value
        value = Round(value * 100)
        
        .Cells(i, "S") = value
        
        If (value = 10) Then
            t4 = t4 + 1
            
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "D") = 1 + Sheets("jingjia2").Cells(6, "D")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "D") = 1 + Sheets("jingjia2").Cells(7, "D")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "D") = 1 + Sheets("jingjia2").Cells(8, "D")
            End If
            
        ElseIf (value = 40) Then
            t4 = t4 + 1
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "D") = 1 + Sheets("jingjia2").Cells(6, "D")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "D") = 1 + Sheets("jingjia2").Cells(7, "D")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "D") = 1 + Sheets("jingjia2").Cells(8, "D")
            End If
        
        ElseIf (value = 45) Then
         t45 = t45 + 1
            
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "E") = 1 + Sheets("jingjia2").Cells(6, "E")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "E") = 1 + Sheets("jingjia2").Cells(7, "E")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "E") = 1 + Sheets("jingjia2").Cells(8, "E")
            End If
        
        ElseIf (value = 50) Then
         t5 = t5 + 1
         
         If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "F") = 1 + Sheets("jingjia2").Cells(6, "F")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "F") = 1 + Sheets("jingjia2").Cells(7, "F")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "F") = 1 + Sheets("jingjia2").Cells(8, "F")
            End If
     
        
        ElseIf (value = 55) Then
         t55 = t55 + 1
      
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "G") = 1 + Sheets("jingjia2").Cells(6, "G")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "G") = 1 + Sheets("jingjia2").Cells(7, "G")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "G") = 1 + Sheets("jingjia2").Cells(8, "G")
            End If
        
        ElseIf (value = 60) Then
         t6 = t6 + 1
            If (.Cells(i, "G") = "CanNotProcess") Then
                    Sheets("jingjia2").Cells(6, "H") = 1 + Sheets("jingjia2").Cells(6, "H")
                    
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "H") = 1 + Sheets("jingjia2").Cells(7, "H")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "H") = 1 + Sheets("jingjia2").Cells(8, "H")
            End If
        
        ElseIf (value = 65) Then
         t65 = t65 + 1
        
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "I") = 1 + Sheets("jingjia2").Cells(6, "I")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "I") = 1 + Sheets("jingjia2").Cells(7, "I")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "I") = 1 + Sheets("jingjia2").Cells(8, "I")
            End If
        
        ElseIf (value = 70) Then
         t7 = t7 + 1
        
        If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "J") = 1 + Sheets("jingjia2").Cells(6, "J")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "J") = 1 + Sheets("jingjia2").Cells(7, "J")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "J") = 1 + Sheets("jingjia2").Cells(8, "J")
            End If
        
        ElseIf (value = 80) Then
         t8 = t8 + 1
            
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "K") = 1 + Sheets("jingjia2").Cells(6, "K")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "K") = 1 + Sheets("jingjia2").Cells(7, "K")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "K") = 1 + Sheets("jingjia2").Cells(8, "K")
            End If
        
        ElseIf (value = 100) Then
         t1 = t1 + 1
         
            If (.Cells(i, "G") = "CanNotProcess") Then
                Sheets("jingjia2").Cells(6, "L") = 1 + Sheets("jingjia2").Cells(6, "L")
                
            ElseIf (.Cells(i, "G") = "Released") Then
                Sheets("jingjia2").Cells(7, "L") = 1 + Sheets("jingjia2").Cells(7, "L")
                
            ElseIf (.Cells(i, "G") = "Reviewing") Then
                Sheets("jingjia2").Cells(8, "L") = 1 + Sheets("jingjia2").Cells(8, "L")
            End If
             
         Else
         
         .Cells(i, "T") = value
         
        End If
        
        Next i
    'MsgBox (row)
    
End With

With Sheets("jingjia2") '填充竞价总量
    Range("D9").value = t4
    Range("E9").value = t45
    Range("F9").value = t5
    Range("G9").value = t55
    Range("H9").value = t6
    Range("I9").value = t65
    Range("J9").value = t7
    Range("K9").value = t8
    Range("L9").value = t1
    Range("M9").value = row
    Range("D10").value = t4 / row
    Range("E10").value = t45 / row
    Range("F10").value = t5 / row
    Range("G10").value = t55 / row
    Range("H10").value = t6 / row
    Range("I10").value = t65 / row
    Range("J10").value = t7 / row
    Range("K10").value = t8 / row
    Range("L10").value = t1 / row
    Range("D10:L10").NumberFormatLocal = "0.00%"
    Range("J19:J24").NumberFormatLocal = "0.00%"
    Range("E19:E24").NumberFormatLocal = "0.00%"
    Range("H19:H24").NumberFormatLocal = "0.00%"
    Range("E29:E34").NumberFormatLocal = "0.00%"
    Range("H29:H34").NumberFormatLocal = "0.00%"
    Range("J29:J34").NumberFormatLocal = "0.00%"
    End With
End Sub


Sub calcStatue()
    With Sheets("jingjia2")
       Range("M6").Formula = "=Sum(D6:L6)"
       Range("M7").Formula = "=Sum(D7:L7)"
       Range("M8").Formula = "=Sum(D8:L8)"
       Range("M9").Formula = "=Sum(D9:L9)"
       
       Range("D25").Formula = "=Sum(D19:D24)"
       Range("G25").Formula = "=Sum(G19:G24)"
       
       Range("D35").Formula = "=Sum(D29:D34)"
       Range("G35").Formula = "=Sum(G29:G34)"
       Range("I35").Formula = "=Sum(I29:I34)"
       
       
       .Cells(19, "I") = .Cells(19, "D").value + .Cells(19, "G")
       .Cells(20, "I") = .Cells(20, "D").value + .Cells(20, "G")
       .Cells(21, "I") = .Cells(21, "D").value + .Cells(21, "G")
       .Cells(22, "I") = .Cells(22, "D").value + .Cells(22, "G")
       .Cells(23, "I") = .Cells(23, "D").value + .Cells(23, "G")
       .Cells(24, "I") = .Cells(24, "D").value + .Cells(24, "G")
       .Cells(25, "I") = .Cells(25, "D").value + .Cells(25, "G")
       
       .Cells(29, "I") = .Cells(29, "D").value + .Cells(29, "G")
       .Cells(30, "I") = .Cells(30, "D").value + .Cells(30, "G")
       .Cells(31, "I") = .Cells(31, "D").value + .Cells(31, "G")
       .Cells(32, "I") = .Cells(32, "D").value + .Cells(32, "G")
       .Cells(33, "I") = .Cells(33, "D").value + .Cells(33, "G")
       .Cells(34, "I") = .Cells(34, "D").value + .Cells(34, "G")
       
       .Cells(19, "E") = .Cells(19, "D") / .Cells(25, "D")
       .Cells(20, "E") = .Cells(20, "D") / .Cells(25, "D")
       .Cells(21, "E") = .Cells(21, "D") / .Cells(25, "D")
       .Cells(22, "E") = .Cells(22, "D") / .Cells(25, "D")
       .Cells(23, "E") = .Cells(23, "D") / .Cells(25, "D")
       .Cells(24, "E") = .Cells(24, "D") / .Cells(25, "D")
       
       .Cells(19, "H") = .Cells(19, "G") / .Cells(25, "G")
       .Cells(20, "H") = .Cells(20, "G") / .Cells(25, "G")
       .Cells(21, "H") = .Cells(21, "G") / .Cells(25, "G")
       .Cells(22, "H") = .Cells(22, "G") / .Cells(25, "G")
       .Cells(23, "H") = .Cells(23, "G") / .Cells(25, "G")
       .Cells(24, "H") = .Cells(24, "G") / .Cells(25, "G")
        
       .Cells(19, "J") = .Cells(19, "I") / .Cells(25, "I")
       .Cells(20, "J") = .Cells(20, "I") / .Cells(25, "I")
       .Cells(21, "J") = .Cells(21, "I") / .Cells(25, "I")
       .Cells(22, "J") = .Cells(22, "I") / .Cells(25, "I")
       .Cells(23, "J") = .Cells(23, "I") / .Cells(25, "I")
        .Cells(24, "J") = .Cells(24, "I") / .Cells(25, "I")
       
       
       .Cells(29, "E") = .Cells(29, "D") / .Cells(35, "D")
       .Cells(30, "E") = .Cells(30, "D") / .Cells(35, "D")
       .Cells(31, "E") = .Cells(31, "D") / .Cells(35, "D")
       .Cells(32, "E") = .Cells(32, "D") / .Cells(35, "D")
       .Cells(33, "E") = .Cells(33, "D") / .Cells(35, "D")
       .Cells(34, "E") = .Cells(34, "D") / .Cells(35, "D")
       
       .Cells(29, "H") = .Cells(29, "G") / .Cells(35, "G")
       .Cells(30, "H") = .Cells(30, "G") / .Cells(35, "G")
       .Cells(31, "H") = .Cells(31, "G") / .Cells(35, "G")
       .Cells(32, "H") = .Cells(32, "G") / .Cells(35, "G")
       .Cells(33, "H") = .Cells(33, "G") / .Cells(35, "G")
       .Cells(34, "H") = .Cells(34, "G") / .Cells(35, "G")
       
       .Cells(29, "J") = .Cells(29, "I") / .Cells(35, "I")
       .Cells(30, "J") = .Cells(30, "I") / .Cells(35, "I")
       .Cells(31, "J") = .Cells(31, "I") / .Cells(35, "I")
       .Cells(32, "J") = .Cells(32, "I") / .Cells(35, "I")
       .Cells(33, "J") = .Cells(33, "I") / .Cells(35, "I")
       .Cells(34, "J") = .Cells(34, "I") / .Cells(35, "I")
       
       Range("E21").Font.ColorIndex = 3
       Range("H21").Font.ColorIndex = 3
       Range("J21").Font.ColorIndex = 3
       Range("E31").Font.ColorIndex = 3
       Range("H31").Font.ColorIndex = 3
       Range("J31").Font.ColorIndex = 3
       
       
       Dim total As Single
       
       total = .Cells(9, "D").value * 0.4 + .Cells(9, "E").value * 0.45 + .Cells(9, "F").value * 0.5 + .Cells(9, "G").value * 0.55 + .Cells(9, "H").value * 0.6 + .Cells(9, "I").value * 0.65 + .Cells(9, "J").value * 0.7 + .Cells(9, "K").value * 0.8 + .Cells(9, "L").value * 1
 
       .Cells(7, "N").value = total / .Cells(9, "M").value
       
    End With
Sheets("jingjia2").Activate
End Sub