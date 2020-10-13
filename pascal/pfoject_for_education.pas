
{$reference 'System.Windows.Forms.dll'}
{$reference 'System.Drawing.dll'} 


uses System.Windows.Forms;
uses System.Drawing;

//names for work: 2 picturebox, 1 rectangle, 2 bitmap, 1 bool
var a1: bool; my_rect: System.Drawing.Rectangle;

//draw rectangle on picturebox
procedure my_draw_rectangle(object sender, System.Windows.Forms.MouseEventArgs e));
begin
  var my_point: Point := new Point(e.X, E.y);
  
end;

begin
  //create app
  var myform: Form := new Form;
  myform.Text := 'wow';
  
  //create picturebox 
  var pic: PictureBox := new PictureBox;
  myform.Controls.Add(pic);
  
  //create new bmp and add to picturebox
  var bit: Bitmap := new Bitmap('hz.png');
  pic.Image := bit;
  
  //work with size
  pic.Size := bit.Size;
  myform.Size := pic.Size;
  //myform.FormBorderStyle := FormBorderStyle.FixedToolWindow;
  
  //work with new picture 
  //1. Create new Rectangle
  //var point_for_rectangle: Point := new Point(300, 300);
  //var size_for_rectangle: Size := new Size(200, 200);
  //var new_rect: Rectangle := new Rectangle(point_for_rectangle, size_for_rectangle);
  
  //2. create new bitmap and his graphics 
  //var bit2: Bitmap := new Bitmap(new_rect.Width, new_rect.Height);
  //var g: Graphics := Graphics.FromImage(bit2);
  //g.DrawImage(bit, 0, 0, new_rect, GraphicsUnit.Pixel);
  
  //3. Add bitmap in form
  //var new_pic: PictureBox := new PictureBox;
  //new_pic.Size := bit2.Size;
  //new_pic.Image := bit2;
  //myform.Controls.Add(new_pic);
  //new_pic.BringToFront;
  
  
  pic.MouseDown += my_draw_rectangle;
  
  
  
  //power app
  Application.Run(myform);
end.














