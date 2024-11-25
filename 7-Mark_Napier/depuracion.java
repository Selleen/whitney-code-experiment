import java.awt.*;
import java.awt.image.*;

public class Bitmap255 extends Component {
    
    // Window size
    private int winWidth, winHeight;
    private int winWidthCenter, winHeightCenter;
    private int maxBitmapIdx;

    // Current frame image producer and associated data
    private MemoryImageSource frameSource;
    private Image curFrame;
    private byte[] frameData;

    // Palette info
    private byte[] palRed;
    private byte[] palGreen;
    private byte[] palBlue;

    // For controlling color changes
    private float targetColorValue = 255.0F; // 0 - 255
    private float opacity = 0.05F; // 0.005 - 1.0
    private int bgColorValue = 40;

    // Bounding box tracking
    private int minX = 0, minY = 0, maxX = 0, maxY = 0;

    public Bitmap255(int width, int height) {
        this.winWidth = width;
        this.winHeight = height;
        this.winWidthCenter = winWidth / 2;
        this.winHeightCenter = winHeight / 2;
    }

    public void init() {
        // Have to setBounds or repaint won't work
        setBounds(0, 0, winWidth, winHeight);

        maxBitmapIdx = (winWidth * winHeight) - 1;
        palRed = new byte[256];
        palGreen = new byte[256];
        palBlue = new byte[256];

        buildPalette(0.0f);

        // Build the Image Buffer
        frameData = new byte[winWidth * winHeight];
        frameSource = new MemoryImageSource(winWidth, winHeight,
                new IndexColorModel(8, 256, palRed, palGreen, palBlue),
                frameData, 0, winWidth);
        frameSource.setAnimated(true);
        curFrame = createImage(frameSource);

        // Set pixels to background color
        Arrays.fill(frameData, (byte) bgColorValue);

        // Reset bounding box to center
        minX = winWidthCenter;
        maxX = winWidthCenter;
        minY = winHeightCenter;
        maxY = winHeightCenter;
        repaint();
    }

    public void setOpacity(float o) {
        if (o >= 0.0 && o <= 1.0) {
            opacity = o;
        }
    }

    public void makeFade(int bR, int bG, int bB, int eR, int eG, int eB, int numsteps) {
        int cR, cG, cB;
        double steps = (double) numsteps;
        for (double currStep = 0.0; currStep < steps; currStep++) {
            cR = (int) ((bR * ((steps - currStep) / steps)) + (eR * (currStep / steps)));
            cG = (int) ((bG * ((steps - currStep) / steps)) + (eG * (currStep / steps)));
            cB = (int) ((bB * ((steps - currStep) / steps)) + (eB * (currStep / steps)));
            // Ensure color components are within bounds
            cR = Math.max(0, Math.min(255, cR));
            cG = Math.max(0, Math.min(255, cG));
            cB = Math.max(0, Math.min(255, cB));

            palRed[(int) currStep] = (byte) cR;
            palGreen[(int) currStep] = (byte) cG;
            palBlue[(int) currStep] = (byte) cB;
        }
    }

    public void buildPalette(float t) {
        makeFade(15, 20, 25, 255, 255, 200, 256);
    }

    @Override
    public void update(Graphics g) {
        paint(g);
    }

    @Override
    public void paint(Graphics g) {
        // Refresh pixels
        frameSource.newPixels(minX, minY, maxX - minX, maxY - minY);
        g.drawImage(curFrame, 0, 0, this);
        // Reset bounding box to center
        minX = winWidthCenter;
        maxX = winWidthCenter;
        minY = winHeightCenter;
        maxY = winHeightCenter;
    }

    // Draw a line to the bitmap
    public synchronized void drawLine(int x1, int y1, int x2, int y2) {
        // Interpolate line points
        int deltaX = Math.abs(x1 - x2);
        int deltaY = Math.abs(y1 - y2);
        int xdirection = (x2 > x1) ? 1 : -1;
        int ydirection = (y2 > y1) ? 1 : -1;
        int xspot, yspot;

        if (deltaX > deltaY) {
            for (int dx = 0; dx <= deltaX; dx++) {
                yspot = (int) ((y1 * ((double) deltaX - dx) / deltaX) + (y2 * (dx / (double) deltaX)));
                xspot = x1 + (xdirection * dx);
                updatePixel(xspot, yspot);
            }
        } else {
            for (int dy = 0; dy <= deltaY; dy++) {
                xspot = (int) ((x1 * ((double) deltaY - dy) / deltaY) + (x2 * (dy / (double) deltaY)));
                yspot = y1 + (ydirection * dy);
                updatePixel(xspot, yspot);
            }
        }

        // Adjust bounding box
        minX = Math.min(minX, Math.min(x1, x2));
        maxX = Math.max(maxX, Math.max(x1, x2));
        minY = Math.min(minY, Math.min(y1, y2));
        maxY = Math.max(maxY, Math.max(y1, y2));
    }

    // Helper method to update pixel data with fade effect
    private void updatePixel(int x, int y) {
        if (x >= 0 && x < winWidth && y >= 0 && y < winHeight) {
            int tmpp = (y * winWidth) + x;
            if (tmpp >= 0 && tmpp < maxBitmapIdx) {
                byte tmpb = frameData[tmpp];
                frameData[tmpp] = (byte) Math.ceil((float) tmpb + ((float) (targetColorValue - tmpb) * opacity));
            }
        }
    }
}
