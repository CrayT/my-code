Sub calculateAIJIA()
    Dim x As New ADODB.Connection
    Dim ds As New ADODB.Recordset
    
    
    If x Is Nothing Then
      Set x = CreateObject("adodb.connection")
      x.Open "", "", ""      'MySQL是在ODBC中Data source Name ;root是用户名 123456 是密码
    ElseIf x.State = 0 Then
      Set x = CreateObject("adodb.connection")
      x.Open "", "", ""
    End If
    
    Dim date0 As String
    Dim date1 As String
    Dim date2 As String
    
    date0 = Sheets("jingjia2").Cells(15, "B").value
    date1 = Sheets("jingjia2").Cells(15, "C").value
    date2 = Sheets("jingjia2").Cells(15, "D").value
    date3 = Sheets("jingjia2").Cells(15, "E").value

    '前一天 cityId=1
    Sql = "SELECT TaskState 状态id,CASE TaskState WHEN '30000' THEN '等待制作'  WHEN '40000' THEN '处理中' WHEN '45000' THEN '待打码' WHEN '50000' THEN '制作成功' WHEN '51000' THEN '制作完成废弃' WHEN '52000' THEN '制作失败' END AS 状态,COUNT(*) AS 套数 FROM housetask WHERE Bucket in('offweb3d04') AND CityId in('1') AND UploadTime BETWEEN  '" & date1 & "'  and  '" & date2 & "'  GROUP BY TaskState;"
    'MsgBox (Sql)
    
    
    '前一天 cityId=2
    Sql2 = "SELECT TaskState 状态id,CASE TaskState WHEN '30000' THEN '等待制作'  WHEN '40000' THEN '处理中' WHEN '45000' THEN '待打码' WHEN '50000' THEN '制作成功' WHEN '51000' THEN '制作完成废弃' WHEN '52000' THEN '制作失败' END AS 状态,COUNT(*) AS 套数 FROM housetask WHERE Bucket in('offweb3d04') AND CityId in('2') AND UploadTime BETWEEN  '" & date1 & "'  and  '" & date2 & "'  GROUP BY TaskState;"
    'MsgBox (Sq2)
    
    
    '本月 cityId=1
    Sql3 = "SELECT TaskState 状态id,CASE TaskState WHEN '30000' THEN '等待制作'  WHEN '40000' THEN '处理中' WHEN '45000' THEN '待打码' WHEN '50000' THEN '制作成功' WHEN '51000' THEN '制作完成废弃' WHEN '52000' THEN '制作失败' END AS 状态,COUNT(*) AS 套数 FROM housetask WHERE Bucket in('offweb3d04') AND CityId in('1') AND UploadTime BETWEEN  '" & date0 & "'  and  '" & date2 & "'  GROUP BY TaskState;"
    'MsgBox (Sql)
    
    '本月 cityId=2
    Sql4 = "SELECT TaskState 状态id,CASE TaskState WHEN '30000' THEN '等待制作'  WHEN '40000' THEN '处理中' WHEN '45000' THEN '待打码' WHEN '50000' THEN '制作成功' WHEN '51000' THEN '制作完成废弃' WHEN '52000' THEN '制作失败' END AS 状态,COUNT(*) AS 套数 FROM housetask WHERE Bucket in('offweb3d04') AND CityId in('2') AND UploadTime BETWEEN  '" & date0 & "'  and  '" & date2 & "'  GROUP BY TaskState;"
    'MsgBox (Sq2)
    
     '当天 cityId=2
    Sql5 = "SELECT TaskState 状态id,CASE TaskState WHEN '30000' THEN '等待制作'  WHEN '40000' THEN '处理中' WHEN '45000' THEN '待打码' WHEN '50000' THEN '制作成功' WHEN '51000' THEN '制作完成废弃' WHEN '52000' THEN '制作失败' END AS 状态,COUNT(*) AS 套数 FROM housetask WHERE Bucket in('offweb3d04') AND CityId in('2') AND UploadTime BETWEEN  '" & date0 & "'  and  '" & date2 & "'  GROUP BY TaskState;"
  
     
     
     '两个城市当月：
     Sql11 = "select ht.CityId,ht.PackageId,ht.CustomerHouseId,ht.TaskState,ht.UploadTime,htn.FirstNotifySuccessTime from housetask as ht left join housetasknotify as htn on ht.Id=htn.HouseTaskId and htn.Type='VRHouse_NotifySelf' where ht.BillOwnerId='1acb8f423db84fe8abc10edb59d25cf0' and ht.CityId in ('1','2') and ht.UploadTime BETWEEN  '" & date0 & "'  and  '" & date2 & "'   and ht.TaskState=50000;"
     
     '两个城市当天：
     Sql111 = "select ht.CityId,ht.PackageId,ht.CustomerHouseId,ht.TaskState,ht.UploadTime,htn.FirstNotifySuccessTime from housetask as ht left join housetasknotify as htn on ht.Id=htn.HouseTaskId and htn.Type='VRHouse_NotifySelf' where ht.BillOwnerId='1acb8f423db84fe8abc10edb59d25cf0' and ht.CityId in ('1','2') and ht.UploadTime BETWEEN  '" & date1 & "'  and  '" & date2 & "'   and ht.TaskState=50000;"
    
     
    Call isExistSheet
     
   '前一天 cityId=1
    With ds
            Set city11 = x.Execute(Sql)
            '.Open Sql, x
            
            Sheets("Sheet2").Select
            Sheets("Sheet2").Cells.Clear
    
            Range("A1").CopyFromRecordset city11 '将结果可以放到单元格内

    End With
    
    
  '前一天 cityId=2
  With ds
  
        Set city12 = x.Execute(Sql2)
        
        Sheets("Sheet2").Select
    
        Range("A11").CopyFromRecordset city12 '将结果可以放到单元格内

  End With
    
    
   '本月 cityId=1
  With ds
  
        Set city21 = x.Execute(Sql3)
    
        Sheets("Sheet2").Select
    
        Range("A21").CopyFromRecordset city21 '将结果可以放到单元格内

  End With


  '本月 cityId=2
 With ds
 
        Set city22 = x.Execute(Sql4)
        
        Sheets("Sheet2").Select
        
        Range("A31").CopyFromRecordset city22 '将结果可以放到单元格内
    
End With


'两个城市当月？
 With ds
 
    Set city3 = x.Execute(Sql11)
    
    Sheets("Sheet3").Select
    Sheets("Sheet3").Cells.Clear
    
    Range("A1").CopyFromRecordset city3 '将结果可以放到单元格内
    
End With


'两个城市当天？
 With ds
 
    Set city4 = x.Execute(Sql111)
    
    Sheets("Sheet4").Select
    Sheets("Sheet4").Cells.Clear
    
    Range("A1").CopyFromRecordset city4 '将结果可以放到单元格内
    
End With



    Call calcTimeGap(date3)
    Call writeAIJIA
    
    
End Sub

Sub writeAIJIA()
    With Sheets("jingjia2")
        
        Dim title As String
        title = "爱家" + .Cells(15, "C") + "至" + .Cells(15, "D") + "上传房源处理时效"
        .Range("C17").value = title
        .Range("C18").value = "备注"
        .Range("C19").value = "处理中"
        .Range("C20").value = "待打码未推送"
        .Range("C21").value = "超时完成"
        .Range("C22").value = "制作成功"
        .Range("C23").value = "制作完成废弃"
        .Range("C24").value = "制作失败"
        .Range("C25").value = "总计"
        
        .Range("D18").value = "北京"
        .Range("E18").value = "占比"
        .Range("F18").value = "备注"
        .Range("G18").value = "杭州"
        .Range("H18").value = "占比"
        .Range("I18").value = "总计"
        .Range("J18").value = "占比"
        .Range("C18:J18").Interior.ColorIndex = 41
        .Range("C17:J17").Interior.ColorIndex = 46
        .Range("C25:J25").Interior.ColorIndex = 41
        
        
        Dim title2 As String
        title2 = "爱家" + .Cells(15, "B") + "至" + .Cells(15, "C") + "上传房源处理时效"
        .Range("C27").value = title2
        .Range("C28").value = "备注"
        .Range("C29").value = "0-24h"
        .Range("C30").value = "24-48h"
        .Range("C31").value = "48h以上"
        .Range("C32").value = "待打码未推送"
        .Range("C33").value = "制作完成被废弃"
        .Range("C34").value = "制作失败无需推送"
        .Range("C35").value = "总计"
        
        .Range("D28").value = "北京"
        .Range("E28").value = "占比"
        .Range("F28").value = "备注"
        .Range("G28").value = "杭州"
        .Range("H28").value = "占比"
        .Range("I28").value = "总计"
        .Range("J28").value = "占比"
        .Range("C28:J28").Interior.ColorIndex = 37
        .Range("C27:J27").Interior.ColorIndex = 46
        .Range("C18:J18").Interior.ColorIndex = 37
        .Range("C25:J25").Interior.ColorIndex = 37
        .Range("C35:J35").Interior.ColorIndex = 37
        
    End With
End Sub


Sub calcTimeGap(date3)

        Dim totalRows As Integer
        Dim totalCols As Integer
        Dim col As Integer
        Dim i As Integer
        
    With Sheets("Sheet3")

        totalRows = .UsedRange.Rows.Count '列

        For i = 1 To totalRows
        
            .Cells(i, 7) = (.Cells(i, 6) - .Cells(i, 5)) * 24
            
        Next i
        
    End With
    
    
    With Sheets("Sheet4")

        totalRows = .UsedRange.Rows.Count '列
        
        For i = 1 To totalRows
        
            .Cells(i, 7) = date3 '补上今日日期
            .Cells(i, 8) = (.Cells(i, 7) - .Cells(i, 6)) * 24 '减去倒数前一列乘以24  前一天

        Next i
        
    End With
    
    
    Call calcTimeOut
    
End Sub


Sub calcTimeOut()


With Sheets("Sheet4")

        Sheets("jingjia2").Range("D19:D24").ClearContents '清空当前几个单元格数据
        Sheets("jingjia2").Range("G19:G24").ClearContents
        
        Sheets("jingjia2").Range("D29:D34").ClearContents '清空当前几个单元格数据
        Sheets("jingjia2").Range("G29:G34").ClearContents
        
        
        Dim totalRows As Integer
        Dim totalCols As Integer

        totalRows = .UsedRange.Rows.Count '列
    
        Dim value As Single
        Dim city As Integer
        
        Dim i As Integer
        Dim beijing As Integer
        Dim hangzhou As Integer
        
        bejing = 0
        hangzhou = 0
        
        For i = 1 To totalRows
            value = .Cells(i, 8).value
            city = .Cells(i, 1).value
            
            If (city = 1) Then '北京
                beijing = beijing + 1
                If (value > 0) Then
                
                    Sheets("jingjia2").Cells(22, "D") = 1 + Sheets("jingjia2").Cells(22, "D")
                
                End If
                
            Else '杭州
                hangzhou = hangzhou + 1
                
                If (value > 0) Then
                
                   Sheets("jingjia2").Cells(22, "G") = 1 + Sheets("jingjia2").Cells(22, "G")
                 End If
           End If
            
                
        Next i

        Sheets("jingjia2").Cells(21, "D") = beijing - Sheets("jingjia2").Cells(22, "D") '超时的
        Sheets("jingjia2").Cells(21, "G") = hangzhou - Sheets("jingjia2").Cells(22, "G") '超时的
        
    End With
    

With Sheets("Sheet2")

    For i = 1 To 10
        value = .Cells(i, 1).value
        If (value = 40000) Then
            Sheets("jingjia2").Cells(19, "D") = .Cells(i, "C").value
        ElseIf (value = 45000) Then
            
            Sheets("jingjia2").Cells(20, "D") = .Cells(i, "C").value
        
        ElseIf (value = 51000) Then
            
            Sheets("jingjia2").Cells(23, "D") = .Cells(i, "C").value
            
       ElseIf (value = 52000) Then
            
            Sheets("jingjia2").Cells(24, "D") = .Cells(i, "C").value
    End If
    
    Next i
    

    For i = 11 To 20
        value = .Cells(i, 1).value
        If (value = 40000) Then
            Sheets("jingjia2").Cells(19, "G") = .Cells(i, "C").value
        ElseIf (value = 45000) Then
            
            Sheets("jingjia2").Cells(20, "G") = .Cells(i, "C").value
        
        ElseIf (value = 51000) Then
            
            Sheets("jingjia2").Cells(23, "G") = .Cells(i, "C").value
            
        ElseIf (value = 52000) Then
            
            Sheets("jingjia2").Cells(24, "G") = .Cells(i, "C").value
    End If
    
    Next i
    

    For i = 21 To 30
        value = .Cells(i, 1).value
        If (value = 45000) Then
        
            Sheets("jingjia2").Cells(32, "D") = .Cells(i, "C").value
            
        ElseIf (value = 51000) Then
            
            Sheets("jingjia2").Cells(33, "D") = .Cells(i, "C").value
        
        ElseIf (value = 52000) Then
            
            Sheets("jingjia2").Cells(34, "D") = .Cells(i, "C").value
    End If
    
    Next i

    For i = 31 To 40
        value = .Cells(i, 1).value
        
        If (value = 45000) Then
        
            Sheets("jingjia2").Cells(32, "G") = .Cells(i, "C").value
            
        ElseIf (value = 51000) Then
            
            Sheets("jingjia2").Cells(33, "G") = .Cells(i, "C").value
        
        ElseIf (value = 52000) Then
            
            Sheets("jingjia2").Cells(34, "G") = .Cells(i, "C").value
    End If
    
    Next i
    
End With


With Sheets("Sheet3")

        totalRows = .UsedRange.Rows.Count '列
        
        bejing = 0
        hangzhou = 0
        
        For i = 1 To totalRows
        
            value = .Cells(i, 7).value
            
            city = .Cells(i, 1).value
            
            If (city = 1) Then '北京
            
                beijing = beijing + 1
                
                If (value > 0 And value <= 24) Then
                
                    Sheets("jingjia2").Cells(29, "D") = 1 + Sheets("jingjia2").Cells(29, "D")
                
                ElseIf (value > 24 And value <= 48) Then
                
                    Sheets("jingjia2").Cells(30, "D") = 1 + Sheets("jingjia2").Cells(30, "D")
                    
                Else
                
                    Sheets("jingjia2").Cells(31, "D") = 1 + Sheets("jingjia2").Cells(31, "D")
                    
                End If
                
            Else '杭州
            
                hangzhou = hangzhou + 1
                
                If (value > 0 And value <= 24) Then
                
                    Sheets("jingjia2").Cells(29, "G") = 1 + Sheets("jingjia2").Cells(29, "G")
                
                ElseIf (value > 24 And value <= 48) Then
                
                    Sheets("jingjia2").Cells(30, "G") = 1 + Sheets("jingjia2").Cells(30, "G")
                    
                Else
                
                    Sheets("jingjia2").Cells(31, "G") = 1 + Sheets("jingjia2").Cells(31, "G")
                    
                 End If
           End If
            
                
        Next i


End With


Call calcStatue '最后计算制作状态
    
End Sub