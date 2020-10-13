
{$reference 'System.Windows.Forms.dll'}
{$reference 'System.Drawing.dll'} 

uses System.Windows.Forms;
uses System.Drawing;

var pic: PictureBox := new PictureBox;
var bit: Bitmap := new Bitmap(200, 200);

var pnt: Point;
procedure ClickMe(sender: object; e: System.EventArgs);
begin
  
end;

begin
  var form: System.Windows.Forms.Form := new Form;
  
  pic.Image := bit;
  pic.Size := bit.Size;
  form.Size := pic.Size;
  
  //work with graph 
  var g: Graphics := Graphics.FromImage(pic.Image);
  g.DrawRectangle(new Pen(Color.Red, 1), 20, 20, 100, 100);
  
  
  
  form.Controls.Add(pic);
  Application.Run(form);
end.


{
uses GraphABC;

var a1: Point;

procedure ClickMe(x,y,mousebutton: integer);
begin
  a1 := new Point(x, y);
end;

procedure my_MouseDown(x,y,mousebutton: integer);
begin
  if mousebutton = 1 then
  begin
    ClearWindow();
    DrawRectangle(a1.X, a1.Y, x, y);
  end;
  //if mousebutton = 0 then ClearWindow();
end;

begin
  OnMouseDown := ClickMe;
  OnMouseMove := my_MouseDown;
end.
}

{uses GraphABC;

procedure MouseDown(x,y,mb: integer);
begin
  MoveTo(x,y);
end;

procedure MouseMove(x,y,mb: integer);
begin
  if mb=1 then LineTo(x,y);
end;

begin
  // Привязка обработчиков к событиям
  OnMouseDown := MouseDown;
  OnMouseMove := MouseMove
end.
}

