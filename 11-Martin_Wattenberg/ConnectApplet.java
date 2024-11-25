import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ConnectApplet extends JPanel implements Runnable {

    Point current;
    Point[] p = new Point[3];
    Thread animation;
    int w, h;
    Image pictureImage;
    Graphics picture;

    public ConnectApplet() {
        w = getWidth();
        h = getHeight();
        pictureImage = createImage(w, h);
        picture = pictureImage.getGraphics();
        p[0] = new Point(w / 2, 100);
        p[1] = new Point(w / 2 + 70, 170);
        p[2] = new Point(w / 2 - 70, 170);
        current = p[0];
        addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                mouseDown(e);
            }
        });
        addMouseMotionListener(new MouseAdapter() {
            public void mouseDragged(MouseEvent e) {
                mouseDrag(e);
            }
        });
    }

    public void start() {
        animation = new Thread(this);
        animation.start();
    }

    public void stop() {
        animation = null;
    }

    public void run() {
        while (animation == Thread.currentThread()) {
            updatePicture();
            repaint();
            try {
                Thread.sleep(20);
            } catch (Exception e) {
            }
        }
    }

    public void update(Graphics g) {
        paint(g);
    }

    public synchronized void paint(Graphics g) {
        g.drawImage(pictureImage, 0, 0, null);
    }

    public void mouseDown(MouseEvent e) {
        int shortest = Integer.MAX_VALUE;
        for (int i = 0; i < p.length; i++) {
            int d2 = (p[i].x - e.getX()) * (p[i].x - e.getX()) + (p[i].y - e.getY()) * (p[i].y - e.getY());
            if (d2 <= shortest) {
                current = p[i];
                shortest = d2;
            }
        }
        mouseDrag(e);
    }

    public void mouseDrag(MouseEvent e) {
        current.x = e.getX();
        current.y = e.getY();
    }

    synchronized void updatePicture() {
        for (int i = 0; i < 5000; i++) {
            int x = (int) (w * Math.random());
            int y = (int) (h * Math.random());
            long a1 = f(p[0], p[1], x, y),
                 a2 = f(p[1], p[2], x, y),
                 a3 = f(p[2], p[0], x, y);
            picture.setColor((int) (a1 * a2 * a3) > 0 ? (a1 * a2 > 0 && a2 * a3 > 0 ? Color.white : Color.gray) : Color.black);
            picture.drawLine(x, y, x, y);
        }
    }

    long f(Point p1, Point p2, int x, int y) {
        return ((p1.x - x) * (p2.y - y) - (p1.y - y) * (p2.x - x)) / 13;
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("ConnectApplet");
        ConnectApplet applet = new ConnectApplet();
        frame.add(applet);
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
        applet.start();
    }
}
