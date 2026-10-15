program scope_rule;
  var x: integer;
  procedure sub1;
  begin
    print(x);
  end;
  procedure sub2;
    var x: integer;
      begin x := 4;
        sub1;
      end;
  begin
      x := 2;
      sub2;
  end;
end.