{$reference 'System.Windows.Forms.dll'}
{$reference 'System.Drawing.dll'} 

uses System.Windows.Forms;
uses System.Drawing;

var bit: Bitmap := new Bitmap('over.png');
var pic: PictureBox := new PictureBox;
var g: Graphics;

var a1: boolean; x1, y1, x2, y2: integer;

procedure my_click(sender: object; e: MouseEventArgs);
begin
  x1 := e.X;
  y1 := e.Y;
end;

procedure my_dclick(sender: object; e: MouseEventArgs);
begin
  x2 := e.X;
  y2 := e.Y;
  g.DrawRectangle(new Pen(Color.Red, 1), x1, y1, x2 - x1, y2 - y1);
end;



begin
  a1 := false;
  var form: Form := new Form;
  pic.Image := bit;
  pic.Size := bit.Size;
  
  
  g := Graphics.FromImage(pic.Image);
  
  
  pic.MouseDown += my_click;
  pic.MouseUp += my_dclick;
  
  
  
  
  form.Controls.Add(pic);
  Application.Run(form);
end.



//2
{
uses System.Windows.Forms;
uses System.Drawing;

begin 
  var form: Form := new Form;
  
  var bit: Bitmap := new Bitmap('over.png');
  var pic: PictureBox := new PictureBox;
  pic.Image := bit;
  pic.Size := bit.Size;
  
  //draw
  var g: Graphics := Graphics.FromImage(pic.Image);
  g.DrawRectangle(new Pen(Color.Red, 1), 20, 20, 100, 100);
  
  
  form.Controls.Add(pic);
  Application.Run(form);
end.
}




//1
{
uses System.Windows.Forms;
uses System.Drawing;

var a1: boolean;
var bit: Bitmap := new Bitmap('over.png');
var pic: PictureBox := new PictureBox;

procedure MyCLick(sender: object; e: MouseEventArgs);
begin
  a1 := true;
end;

procedure MyDown(sender: object; e: MouseEventArgs);
begin
  if a1 = true then pic.Location := new Point(e.X, e.Y);
end;

procedure my_MouseUp(sender: object; e: MouseEventArgs);
begin
  a1 := false;
end;



begin
  var form: System.Windows.Forms.Form := new Form;
  
  
  
  pic.Size := bit.Size;
  pic.Image := bit;
  form.Controls.Add(pic);
  
  pic.MouseDown += MyCLick;
  pic.MouseMove += MyDown;
  pic.MouseUp += my_MouseUp;
  
  
  
  Application.Run(form);
end.
}






