program scope_rule;

  var x: integer;

  procedure sub1;
  begin
    writeln(x);   // 파스칼에서는 print가 아닌 write를 사용.
  end;

  procedure sub2;
  var x: integer;
  begin x := 4;
    sub1;
  end;

  begin
    x := 2;
    sub2;
  end.