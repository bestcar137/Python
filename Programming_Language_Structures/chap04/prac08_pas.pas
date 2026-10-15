program ex(output);
  var x, y: integer; // 전역 변수
  procedure swap(var A, B: integer);
    var temp: integer; // 지역 변수

  begin
    temp := A;
    A := B;
    B := temp;
  end;

  begin
    x := 5; y := -3;
    swap (x, y);
  end.
