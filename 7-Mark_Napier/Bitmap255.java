
//Bitmap255.java

import java.awt.*;
import java.awt.image.*;


// A Bitmap with 255 color palette.
// Functions drawLine() and fillRect() draw transluscent
// line and rect into the bitmap.  BuildPalette() creates
// a palette of 255 colors (fade from fg color to bg color).


public class Bitmap255 extends Component
{
  // Window size
  int winWidth, winHeight;
  int winWidthCenter, winHeightCenter;
  int maxBitmapIdx;

  // Current frame image producer and associated data
  MemoryImageSource frameSource;
  Image curFrame;
  byte[] frameData;

  // Palette info
  byte[] palRed;
  byte[] palGreen;
  byte[] palBlue;

  // tmp vals for calculations
  int tmpp;
  int tmpb;

  // To control color changes dark to lite
 	float targetColorValue = 255.0F;    // 0 - 255
  float opacity = .05F;               // 0.005 - 1.0
  int bgColorValue = 40;

  // for tracking bounding box
  int minX=0, minY=0, maxX=0, maxY=0;


  public Bitmap255(int width, int height) {
    winWidth = width;
    winHeight = height;
    winWidthCenter = winWidth/2;
    winHeightCenter = winHeight/2;
  }


  public void init() {
    // have to setbounds or repaint won't work
    setBounds(0,0,winWidth,winHeight);

    maxBitmapIdx = (winWidth*winHeight) - 1;
    palRed = new byte[256];
    palGreen = new byte[256];
    palBlue = new byte[256];

    buildPalette(0.0f);

    // Build the Image Buffer
    // Framedata holds image pixel data (bytes)
    // Framesource produces an image (curFrame) from Framedata
    frameData = new byte[winWidth*winHeight];
    frameSource = new MemoryImageSource(winWidth,winHeight,
                                        new IndexColorModel(8,256,palRed,palGreen,palBlue),
                                        frameData,0,winWidth);
    frameSource.setAnimated(true);
    curFrame = createImage(frameSource);

    // set pixels to background color
    for (int y=0; y < winHeight; y++) {
      for (int x=0; x < winWidth; x++) {
        tmpp = (y*winWidth)+x;
        frameData[tmpp] = (byte)bgColorValue;
      }
    }

    // reset bounding box to center
    minX = winWidthCenter;
    maxX = winWidthCenter;
    minY = winHeightCenter;
    maxY = winHeightCenter;
    repaint();
  }


  public void setOpacity(float o) {
    if (opacity >= 0.0 && opacity <= 1.0) {
      opacity = o;
    }
  }


  public void makeFade(int bR, int bG, int bB, int eR, int eG, int eB, int numsteps)
  {
      int cR, cG, cB;
      double steps = (double)numsteps;
      for (double currStep=0.0; currStep < steps; currStep++) {
         cR = (int)( (bR * ((steps-currStep)/steps) + (eR * (currStep/steps))) );
         cG = (int)( (bG * ((steps-currStep)/steps) + (eG * (currStep/steps))) );
         cB = (int)( (bB * ((steps-currStep)/steps) + (eB * (currStep/steps))) );
         if (cR > 255 || cG > 255 || cB > 255) {
            System.out.println("FADE OUT OF BOUNDS cR=" + cR +  " cG=" + cG + " cB=" + cB);
         }
         if (cR < 0 || cG < 0 || cB < 0) {
            System.out.println("FADE NEGATIVE cR=" + cR +  " cG=" + cG + " cB=" + cB);
         }
         palRed[(int)currStep] = (byte)cR;
         palGreen[(int)currStep] = (byte)cG;
         palBlue[(int)currStep] = (byte)cB;
      }
  }


  public void buildPalette(float t) {
    makeFade( (int)(15),
              (int)(20),
              (int)(25),
              (int)(255),
              (int)(255),
              (int)(200),
              256);
  }


  public void update( Graphics g ) {
    paint(g);
  }


  public void paint(Graphics g){
    // refresh pixels
    frameSource.newPixels(minX,minY, maxX-minX, maxY-minY);    // update curFrame image
    g.drawImage(curFrame,0,0,this);
    // reset bounding box to center
    minX = winWidthCenter;
    maxX = winWidthCenter;
    minY = winHeightCenter;
    maxY = winHeightCenter;
  }


  // Draw a line to the bitmap
  //
  public synchronized void drawLine( int x1, int y1, int x2, int y2 )
  {
    // Interpolate line points
    int deltaX = Math.abs(x1 - x2);
    int deltaY = Math.abs(y1 - y2);
    int xdirection = (x2 > x1)? 1: -1;
    int ydirection = (y2 > y1)? 1: -1;
    int xspot = 0;
    int yspot = 0;
    if ( deltaX > deltaY ) {
      for(int dx=0; dx <= deltaX; dx++) {
        yspot = (int)Math.floor( (double)y1 * (((double)deltaX-(double)dx)/(double)deltaX) + (double)y2 * ((double)dx/(double)deltaX) );
        xspot = x1 + (xdirection * dx);
        if (yspot >= 0 && yspot < winHeight && xspot >=0 && xspot <=winWidth) {
          tmpp = (yspot*winWidth)+xspot;
          if (tmpp > 0 && tmpp < maxBitmapIdx) {
            tmpb = (int) (frameData[tmpp] & 0xFF);
            frameData[tmpp] = (byte) Math.ceil((float)tmpb + ((float)(targetColorValue-tmpb)*opacity) );
          }
        }
      }
    }
    else {
      for(int dy=0; dy <= deltaY; dy++) {
        xspot = (int)Math.floor( (double)x1 * (((double)deltaY-(double)dy)/(double)deltaY) + (double)x2 * ((double)dy/(double)deltaY) );
        yspot = y1 + (ydirection * dy);
        if (yspot >= 0 && yspot < winHeight && xspot >=0 && xspot <=winWidth) {
          tmpp = (yspot*winWidth)+xspot;
          if (tmpp > 0 && tmpp < maxBitmapIdx) {
            tmpb = (int) (frameData[tmpp] & 0xFF);
            frameData[tmpp] = (byte) Math.ceil((float)tmpb + ((float)(targetColorValue-tmpb)*opacity) );
          }
        }
      }
    }
    // adjust bounding box
    if (x1 < minX) minX = x1; else if (x1 > maxX) maxX = x1;
    if (x2 < minX) minX = x2; else if (x2 > maxX) maxX = x2;
    if (y1 < minY) minY = y1; else if (y1 > maxY) maxY = y1;
    if (y2 < minY) minY = y2; else if (y2 > maxY) maxY = y2;
  }


  // Fill a rectangle into the bitmap
  //
  public synchronized void fillRect_(int x, int y, int w, int h)
  {
    int fadeRadius = 2;
    int y1 = 0;
    int x1 = 0;
    for (y1=(int)y-fadeRadius; y1 < y+fadeRadius; y1++) {
      for (x1=(int)x-fadeRadius; x1 < x+fadeRadius; x1++) {
        tmpp = (y1*winWidth)+x1;
        if (tmpp > 0 && tmpp < maxBitmapIdx) {
          tmpb = (int) (frameData[tmpp] & 0xFF);
          frameData[tmpp] = (byte) Math.ceil((float)tmpb + ((float)(targetColorValue-tmpb)*opacity) );
        }
      }
    }
  }

}
